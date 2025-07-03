# -*- coding: utf-8 -*-
"""执行优惠计算和结算流程"""

import time
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_root)

from Aoeo.common.Logger import EnhancedLogger
from Aoeo.testcases.getMemberDiscount import DiscountService
from Aoeo.testcases.settlementTransactions import SettlementService
from Aoeo.common.TokenGenerator import TokenGenerator
from concurrent.futures import ThreadPoolExecutor

logger = EnhancedLogger()

def process_user(user_id, coupon_codes=None):
    """处理单个用户的测试流程"""
    token_gen = TokenGenerator(algorithm='md5')
    discount_service = DiscountService(token_gen)
    settlement_service = SettlementService(token_gen)

    with token_gen.user_context(user_id):
        logger.info(f"开始测试用户: {user_id}")
        start_time = time.time()

        try:
            # 步骤1: 优惠计算
            discount_res = discount_service.getMemberDiscount(user_id)
            coupon_codes = discount_service.discountResponse(discount_res, user_id)
            logger.info(f"优惠计算返回的coupon_codes: {coupon_codes}")


            # 步骤2: 结算交易 (传递优惠券)
            settle_res = settlement_service.settlementTransactions(
                user_id,
                coupon_codes = coupon_codes)
            logger.info(f"结算交易 (传递优惠券)完成返回的coupon_codes：{coupon_codes}")

            settlement_service.process_response(settle_res, user_id)

        except Exception as e:
            logger.error(f"用户 {user_id} 流程失败: {str(e)}")
        finally:
            elapsed = time.time() - start_time
            logger.info(f"用户 {user_id} 完成, 耗时: {elapsed:.2f}s")


def main(user_id_list, coupon_codes=None, max_workers=3):
    """主执行函数 (支持并发)"""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(lambda uid: process_user(uid, coupon_codes), user_id_list)


if __name__ == "__main__":
    # ====================== 参数配置区 ======================
    USER_ID_LIST = [1900413066794]
    MAX_WORKERS = 3  # 并发线程数
    # ======================================================

    main(
        user_id_list=USER_ID_LIST,
        max_workers=MAX_WORKERS
    )


















"""
def main(userId):
# 初始化Token生成器
TokenGenerator = TokenGenerator(algorithm='md5')
discount_service = DiscountService(TokenGenerator)
settlement_service = SettlementService(TokenGenerator)

user_id_list = [1900413066794]

# 遍历用户执行接口测试
for userId in user_id_list:
    print(f"\n{'=' * 40}")
    print(f"测试用户: {userId}")

with TokenGenerator.user_context(userId):
    # 执行接口调用
    responseData = discount_service.getMemberDiscount(userId)
    response_data = settlement_service.settlementTransactions(userId)

    # 处理响应
    discount_service.discountResponse(responseData, userId)
    settlement_service.process_response(response_data, userId)


if __name__ == "__main__":
    # ====================== 参数配置区 ======================

    # 执行主流程
    # main(user_id=user_id, coupon_code=COUPON_CODE)
    main(userId=userId)"""