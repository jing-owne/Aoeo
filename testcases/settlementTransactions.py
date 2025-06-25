# -*- coding: utf-8 -*-

"""结算交易接口"""
import requests
from Aoeo.common.Logger import EnhancedLogger
from Aoeo.common.TokenGenerator import TokenGenerator
from getMemberDiscount import DiscountService

# 初始化日志
logger = EnhancedLogger()
POS_BASE_URL = 'https://lawsonpos-dev.yorentown.com/pos/v1/pos/'


class SettlementService:
    """结算交易服务封装类"""

    def __init__(self, token_generator):
        self.token_generator = token_generator
        self.interfaces = {"结算交易": "settlementTransactions"}  # 接口映射关系

    def settlementTransactions(self, user_id,coupon_codes=None):
        """发送结算交易请求，coupon_codes依赖优惠确认的传递"""
        try:
            # 动态生成token
            token = self.token_generator.generate_token(
                self.interfaces["结算交易"]
            )

            # 动态构建URL
            url = f"{POS_BASE_URL}settlementTransactions"

            payload = (
                f'accessToken={token}&userCode={user_id}&shopCode=208888&'
                'posNo=72&serialNumber=703165502&paymentAmount=16&'
                'commodityInfoList=[{"totalAmount":31.5,"quantity":5,"commodityBarcode":"056227","price":89,"discountInfoList":[{"discountAmount":89,"discountQuantity":1}],"totalDiscount":89,"noOnlineDiscount":0},{'
                '"totalAmount":60,"quantity":1,"commodityBarcode":"202216","price":60,"discountInfoList":[],"totalDiscount":0,"noOnlineDiscount":0},{'
                '"totalAmount":6,"quantity":1,"commodityBarcode":"044041","price":6,"discountInfoList":[],"totalDiscount":0,"noOnlineDiscount":0}]&'
                'paymentInfoList=[{"paymentType":"050", "paymentTypeAmount":33, "paymentMerchantID":"wxf38e1f7d918ba13f","paymentUserID":"41306679"}]&'
                f'couponCode={coupon_codes}7D&extraInfo={"memberAmount":0}'
            )


            headers = {'Content-Type': 'application/x-www-form-urlencoded'}

            response = requests.post(url, headers=headers, data=payload, timeout=10)
            response.raise_for_status()  # 自动处理HTTP错误

            # 记录响应日志
            logger.info(f"用户 {user_id} 响应状态: {response.status_code}")
            if response.text:
                logger.debug(f"响应内容: {response.text[:200]}...")  # 截断长内容

            return response.json()  # 返回结构化数据

        except requests.exceptions.RequestException as e:
            logger.error(f"用户 {user_id} 请求失败: {str(e)}")
            return None

    def process_response(self, response_data, user_id):
        """处理结算交易响应数据"""
        if not response_data:
            print(f"⚠️ 用户 {user_id} 接口响应失败，请检查日志")
            return False

        print(f"\n用户 {user_id} 结算接口响应成功！")
        result_code = response_data.get('resultCode', 'N/A')
        if result_code == 301:
            return result_code
        campaign_info = response_data.get('campaignInfo', 'N/A')

        print(f"    ✅ 结算接口resultCode: {result_code}")
        print(f"    ✅ 参与的集点活动campaignInfo: {campaign_info}")
        return None

# if __name__ == "__main__":
#     # 初始化Token生成器
#     token_gen = TokenGenerator(algorithm='md5')
#     settlement_service = SettlementService(token_gen)
#
#     # 测试用户列表
#     user_id_list = [1900413066794, 1900413066795, 1900413066796]
#
#     # 遍历用户执行接口测试
#     for user_id in user_id_list:
#         print(f"\n{'=' * 40}")
#         print(f"测试用户: {user_id}")
#
#         # 设置当前用户上下文
#         with token_gen.user_context(user_id):
#             # 执行接口调用
#             response_data = settlement_service.settlement_transactions(user_id)
#
#             # 处理响应
#             settlement_service.process_response(response_data, user_id)
