import smtplib
import os
from dotenv import load_dotenv


load_dotenv()

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
PASSWORD = os.getenv('EMAIL_PASSWORD')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')


def send_confirmation(order, order_id):
    to_email = order.get('email')
    mail_lib = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    mail_lib.login(EMAIL_ADDRESS, PASSWORD)

    body = render_body(order, order_id)

    for addr in [to_email, ADMIN_EMAIL]:
        msg = 'From: %s\r\nTo: %s\r\nContent-Type: text/html; charset="utf-8"\r\nSubject: %s\r\n\r\n' % (
            EMAIL_ADDRESS, addr, 'Mallakto: подтверждение заказа')
        msg += body
        mail_lib.sendmail(EMAIL_ADDRESS, addr, msg.encode('utf8'))

    mail_lib.quit()


def render_body(order, order_id):
    order_items = order.get('order')
    order_table = ''
    for item in order_items:
        order_table += f'''<tr style="border: 1px solid black;">
              <td style="border: 1px solid black;padding: 10px;">{item.get('title')}</td>
              <td style="border: 1px solid black;padding: 10px;">{item.get('quantity')}</td>
              <td style="border: 1px solid black;padding: 10px;">{item.get('price')}</td>
            </tr>'''

    message = f'''<h1>Заказ №{order_id}</h1>
<table style="border: 1px solid black;
      border-collapse: collapse;text-align: center;">
        <tr style="border: 1px solid black;">
          <th style="border: 1px solid black; padding: 10px;font-size:18px;">Наименование</th>
          <th style="border: 1px solid black; padding: 10px;font-size:18px;">Кол-во</th>
          <th style="border: 1px solid black; padding: 10px;font-size:18px;">Цена</th>
        </tr>
        {order_table}
      </table>
      <h2>Конактные данные</h2>
      <p><strong>Имя:<strong> {order.get('nameInput')}</p>
      <p><strong>Телефон:<strong> {order.get('phone')}</p>
      <p><strong>Способ доставки:<strong> {order.get('delivery')}</p>
      <p><strong>Адрес:</strong> {order.get('address', '')}</p>
      <p><strong>Способ оплаты:<strong> {order.get('payment')}</p>'''

    return message
