from ninja import Router, Schema, Query
import hmac
import hashlib
from datetime import datetime

from payment.vnpay import vnpay
from django.conf import settings
from django.http import JsonResponse

payment_router = Router()


class PaymentQuerySchema(Schema):
    order_type: str = "bilpayment"
    order_id: str = "123456"
    amount: int = 10000
    order_desc: str = "Description"
    bank_code: str = "NCB"
    language: str = "vn"


def hmacsha512(key, data):
    byteKey = key.encode("utf-8")
    byteData = data.encode("utf-8")
    return hmac.new(byteKey, byteData, hashlib.sha512).hexdigest()


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


@payment_router.post("/create_payment_url")
def create_payment_url(request, query: PaymentQuerySchema = Query(...)):
    order_type = query.order_type
    order_id = query.order_id
    amount = query.amount
    order_desc = query.order_desc
    bank_code = query.bank_code
    language = query.language
    ipaddr = get_client_ip(request)
    # Build URL Payment
    vnp = vnpay()
    vnp.requestData["vnp_Version"] = "2.1.0"
    vnp.requestData["vnp_Command"] = "pay"
    vnp.requestData["vnp_TmnCode"] = settings.VNPAY_TMN_CODE
    vnp.requestData["vnp_Amount"] = amount * 100
    vnp.requestData["vnp_CurrCode"] = "VND"
    vnp.requestData["vnp_TxnRef"] = order_id
    vnp.requestData["vnp_OrderInfo"] = order_desc
    vnp.requestData["vnp_OrderType"] = order_type
    # Check language, default: vn
    if language and language != "":
        vnp.requestData["vnp_Locale"] = language
    else:
        vnp.requestData["vnp_Locale"] = "vn"
        # Check bank_code, if bank_code is empty, customer will be selected bank on VNPAY
    if bank_code and bank_code != "":
        vnp.requestData["vnp_BankCode"] = bank_code

    vnp.requestData["vnp_CreateDate"] = datetime.now().strftime(
        "%Y%m%d%H%M%S"
    )  # 20150410063022
    vnp.requestData["vnp_IpAddr"] = ipaddr
    vnp.requestData["vnp_ReturnUrl"] = settings.VNPAY_RETURN_URL
    vnpay_payment_url = vnp.get_payment_url(
        settings.VNPAY_PAYMENT_URL, settings.VNPAY_HASH_SECRET_KEY
    )

    return JsonResponse({"payment_url": vnpay_payment_url}, status=200)
