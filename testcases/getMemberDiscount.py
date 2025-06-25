# -*- coding: utf-8 -*-
"""优惠确认接口"""
from jsonpath_ng import parse
import requests
from Aoeo.common.Logger import EnhancedLogger
from Aoeo.common.TokenGenerator import TokenGenerator

# 初始化日志
logger = EnhancedLogger()
POS_BASE_URL = 'https://lawsonpos-dev.yorentown.com/pos/v1/pos/'

class DiscountService:
    """会员折扣服务封装类"""
    def __init__(self, tokenGenerator):
        self.token_generator = tokenGenerator
        self.interfaces = {"优惠确认": "membershipVerification"}


    def getMemberDiscount(self, user_id):
        """发送会员折扣请求（修复版）"""
        try:
            # 动态构建URL
            URL = f"{POS_BASE_URL}getMemberDiscount"

            # 动态生成token
            token = self.token_generator.generate_token(
                self.interfaces["优惠确认"]
            )

            payload = (
                f'accessToken={token}&userCode={user_id}&shopCode=208888&'
                'posNo=84&serialNumber=703165502&paymentAmount=6&posVersion=2&'
                'extraInfo={"memberAmount":0}&'
                'commodityList=[{'
                '"totalAmount":31.5,"quantity":5,"commodityBarcode":"056227","price":89,"discountInfoList":[{"discountAmount":89,"discountQuantity":1}],totalDiscount":89,"noOnlineDiscount":0},{'
                '"totalAmount":60,"quantity":1,"commodityBarcode":"202216","price":60,"discountInfoList":[],"totalDiscount":0,"noOnlineDiscount":0},{'
                '"totalAmount":6,"quantity":2,"commodityBarcode":"044041","price":3,"discountInfoList":[],"totalDiscount":0,"noOnlineDiscount":0}'
                ']'
            )

            headers = {'Content-Type': 'application/x-www-form-urlencoded'}

            response = requests.post(URL, headers=headers, data=payload, timeout=10)
            response.raise_for_status()

            # 记录响应日志
            logger.info(f"响应状态: {response.status_code}")
            if response.text:
                logger.debug(f"响应内容: {response.text[:200]}...")

            return response.json()  # 返回结构化数据

        except requests.exceptions.RequestException as e:
            logger.error(f"请求失败: {str(e)}")
            return None


    def discountResponse(self, responseData, userId):
        """处理接口响应数据"""
        if not responseData:
            print("⚠️ 接口测试失败，请检查日志")
            return None
        print(f"用户 {userId} 优惠确认接口响应成功！返回数据:\n    ✅{responseData}")

        if userInfo := responseData.get('userInfo', []):
            first_user_info = userInfo[0] if userInfo else {}
            user_code = first_user_info.get('userCode', 'N/A')
            userName = first_user_info.get('userName', 'N/A')
            # couponInfoList = responseData.get('couponInfoList','N/A')

            print(f"    ✅ 返回的userName: {userName}")
            print(f"    ✅ 返回的userCode: {user_code}")
            # print(f"    ✅ 返回的券列表couponInfoList: {couponInfoList}")

        # 使用递归搜索提取所有couponCode（无视嵌套层级）
        coupon_expr = parse("$..couponCode")  # 双点号表示递归搜索
        coupon_matches = coupon_expr.find(responseData)
        coupon_code = [match.value for match in coupon_matches]
        if coupon_code:
            coupon_codes = ",".join(coupon_code)
            print(f"    ✅ 提取优惠券ID: {coupon_codes}")
            return coupon_codes
        else:
            print("⚠️ 接口响应但是未找到优惠券")

        resultCode = responseData.get('resultCode', '字段未找到')
        if resultCode == 100 and coupon_code is []:
            userInfo = responseData.get('userInfo', [])
            # print(f"接口响应成功！返回数据{userInfo}")
            return resultCode

        else:
            print(f"    ⚠️响应{resultCode} 用户{userId}未找到！请核对用户条码")
        return False

#
# if __name__ == "__main__":
#     # 初始化Token生成器
#     TokenGenerator = TokenGenerator(algorithm='md5')
#     discount_service = DiscountService(TokenGenerator)
#
#     user_id_list = [1900413066794]
#
#     # 遍历用户执行接口测试
#     for user_id in user_id_list:
#         print(f"\n{'=' * 40}")
#         print(f"测试用户: {user_id}")
#
#         with TokenGenerator.user_context(user_id):
#             # 执行接口调用
#             responseData = discount_service.getMemberDiscount(user_id)
#
#             # 处理响应
#             discount_service.discountResponse(responseData, user_id)

"""          
是打算把请求头作为一个变量传入到这里  
payload = (
                f'accessToken={token}&userCode={user_id}&shopCode={shopCode}&'
                f'posNo={posNo}&serialNumber={serialNumber}&paymentAmount={paymentAmount}&posVersion=2&'
                'extraInfo={"memberAmount":0}&'
                f'commodityList={commodityList}'
            )
            """