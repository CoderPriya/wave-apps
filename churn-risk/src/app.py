from h2o_wave import Q, ui, app, main

import pandas as pd
from .utils import python_code_content
from .plots import html_pie_of_target_percent, wide_stat_card_dollars, tall_stat_card_dollars, get_image_from_matplotlib
from .config import Configuration
from .churn_predictor import ChurnPredictor

config = Configuration()
churn_predictor = ChurnPredictor()

def profile_content():
    df = pd.read_csv(config.testing_data_url).head(40)

    choices = [ui.choice(name=phone, label=f'{phone}') for phone in df[config.id_column]]

    items = [
        ui.text_xl(f'Customer Profiles from {config.get_analysis_type()}'),
        ui.picker(name='customers', label=f'Customer Phone Number', choices=choices, max_choices=1,
                  tooltip='Start typing to search for a customer'),
        ui.button(name='select_customer_button', label='Submit', primary=True)
    ]
    return items

async def profile_selected_page(q: Q):
    del q.page["content"]
    df = pd.read_csv(config.testing_data_url)

    cust_phone_no = q.args.customers[0]
    q.client.selected_customer_index = int(df[df[config.id_column] == cust_phone_no].index[0])

    await populate_customer_churn_stats(cust_phone_no, df, q)

    await populate_churn_plots(q)


async def populate_churn_plots(q):
    shap_plot = churn_predictor.get_shap_explanation(q.client.selected_customer_index)
    q.page['shap_plot'] = ui.image_card(
        box=config.boxes['shap_plot'],
        title='',
        type='png',
        image=get_image_from_matplotlib(shap_plot),
    )
    top_negative_pd_plot = churn_predictor.get_top_negative_pd_explanation(q.client.selected_customer_index)
    q.page['top_negative_pd_plot'] = ui.image_card(
        box=config.boxes['top_negative_pd_plot'],
        title='',
        type='png',
        image=get_image_from_matplotlib(top_negative_pd_plot),
    )
    top_positive_pd_plot = churn_predictor.get_top_positive_pd_explanation(q.client.selected_customer_index)
    q.page['top_positive_pd_plot'] = ui.image_card(
        box=config.boxes['top_positive_pd_plot'],
        title='',
        type='png',
        image=get_image_from_matplotlib(top_positive_pd_plot),
    )


async def populate_customer_churn_stats(cust_phone_no, df, q):

    df['Total Charges'] = df.Total_Day_charge + df.Total_Eve_Charge + df.Total_Night_Charge + df.Total_Intl_Charge

    df = df[["Total_Day_charge", "Total_Eve_Charge", "Total_Night_Charge", "Total_Intl_Charge", config.id_column,
             "Total Charges"]]

    df.columns = ["Day Charges", "Evening Charges", "Night Charges", "Int'l Charges", config.id_column, "Total Charges"]

    q.page["day_stat"] = wide_stat_card_dollars(df, cust_phone_no, "Day Charges", config.boxes['day_stat'],
                                                config.color)
    q.page["eve_stat"] = wide_stat_card_dollars(df, cust_phone_no, "Evening Charges", config.boxes['eve_stat'],
                                                config.color)
    q.page["night_stat"] = wide_stat_card_dollars(df, cust_phone_no, "Night Charges", config.boxes['night_stat'],
                                                  config.color)
    q.page["intl_stat"] = wide_stat_card_dollars(df, cust_phone_no, "Int'l Charges", config.boxes['intl_stat'],
                                                 config.color)
    q.page["total_stat"] = tall_stat_card_dollars(df, cust_phone_no, "Total Charges", config.boxes['total_stat'],
                                                  config.total_gauge_color)
    q.page['customer'] = ui.small_stat_card(box=config.boxes['customer'], title='Customer', value=str(cust_phone_no))

    q.page['churn_rate'] = ui.small_stat_card(box=config.boxes['churn_rate'], title='Churn Rate',
                                              value=str(churn_predictor.get_churn_rate_of_customer(
                                                  q.client.selected_customer_index)) + ' %')

    labels = ["Day Charges", "Evening Charges", "Night Charges", "Int'l Charges"]
    values = [df[df[config.id_column] == cust_phone_no][labels[0]].values[0],
              df[df[config.id_column] == cust_phone_no][labels[1]].values[0],
              df[df[config.id_column] == cust_phone_no][labels[2]].values[0],
              df[df[config.id_column] == cust_phone_no][labels[3]].values[0]]

    q.page['stat_pie'] = ui.frame_card(box=config.boxes['stat_pie'], title='Total call charges breakdown',
                                       content=html_pie_of_target_percent('', labels, values))


async def initialize_page(q: Q):

    content = []

    if not q.client.app_initialized:
        churn_predictor.build_model(config.training_data_url)
        churn_predictor.set_testing_data_frame(config.testing_data_url)
        churn_predictor.predict()

        q.app.header_png, = await q.site.upload([config.image_path])
        q.app.training_file_url, = await q.site.upload([config.working_data])
        content = profile_content()
        q.client.app_initialized = True

    q.page.drop()

    q.page['title'] = ui.header_card(
        box=config.boxes['banner'],
        title=config.title,
        subtitle=config.subtitle,
        icon=config.icon,
        icon_color=config.color,
    )

    q.page['nav_bar'] = ui.form_card(
        box=config.boxes['navbar'],
        items=[
            ui.tabs(name="menu", value=q.args.menu, items=[
                ui.tab(name='profile', label='Customer Profiles'),
                ui.tab(name='tour', label='Application Code')])
        ],
    )
    q.page['content'] = ui.form_card(
        box=config.boxes['content'],
        items=content
    )

    await q.page.save()


@app('/')
async def serve(q: Q):

    await initialize_page(q)
    content = q.page["content"]

    if q.args.select_customer_button:
        await profile_selected_page(q)

    else:
        tab = q.args['menu']

        if tab == 'profile':
            content.items = profile_content()

        elif tab == 'tour':
            content.items = python_code_content('app.py')

    await q.page.save()
