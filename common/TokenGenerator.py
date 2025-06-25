import hashlib
from Logger import EnhancedLogger
# 先创建实例，再调用方法
logger = EnhancedLogger()  # 实例化

class TokenGenerator:
    """修复版Token生成器，彻底解决类型问题"""
    INTERFACE_CONFIG = {
        "membershipVerification": ("membershipVerification", "lawson"),
        "settlementTransactions": ("settlementTransactions", "lawson"),
        "returnInformation": ("returnInformation", "lawson"),
        "couponCorrection": ("couponCorrection", "lawson")
    }

    def __init__(self, algorithm='md5'):
        self.algorithm = algorithm.lower()
        if self.algorithm not in ['md5', 'sha1', 'sha256']:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

    def generate_token(self, interface_key: str, user_code: str) -> str:
        """核心修复：直接使用字符串key访问配置"""
        prefix, middle = self.INTERFACE_CONFIG[interface_key]
        original_str = f"{prefix}{middle}{user_code}"

        # 动态选择算法
        hash_obj = hashlib.new(self.algorithm)
        hash_obj.update(original_str.encode('utf-8'))
        return hash_obj.hexdigest().lower()


# ===== 测试验证 =====
if __name__ == "__main__":
    generator = TokenGenerator(algorithm='md5')
    user_id_list = [1900413066794,1900000000118,1900000000132]

    for user_id in user_id_list:
        user_id_str = str(user_id)
        print(f"\n用户 {user_id} 的Token:")

        # 直接传递字符串key（不再用枚举）
        interfaces = {
            "优惠接口": "membershipVerification",
            "结算接口": "settlementTransactions",
            "退货接口": "returnInformation",
            "冲正接口": "couponCorrection"
        }

        for name, key in interfaces.items():
            token = generator.generate_token(key, user_id_str)
            # print(f"\n用户 {user_id} 的接口Tokens:")
            # logger.info(f"{user_id}{name}: {token}")
            print(f"   {name}: {token}")

    # # 获取所有支持的接口类型
    # print("\n支持的接口类型:")
    # for interface in generator.get_interface_types():
    #     print(f"- {interface.name}: {interface.value}")
    # 生成各接口Token
