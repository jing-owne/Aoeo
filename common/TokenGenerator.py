import hashlib
from Aoeo.common.Logger import EnhancedLogger
from typing import Dict, Callable
from contextlib import contextmanager

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
        self._user_id_getter: Callable[[], str] = None  # 存储用户ID获取函数
        self._context_user_id: str = None  # 上下文中的用户ID

        if self.algorithm not in ['md5', 'sha1', 'sha256']:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

    def register_user_id_getter(self, getter_func: Callable[[], str]):
        """注册用户ID获取函数（依赖注入）"""
        self._user_id_getter = getter_func
        return self  # 支持链式调用


    @contextmanager
    def user_context(self, user_id: str):
        """上下文管理器：临时设置用户ID"""
        original_user_id = self._context_user_id
        self._context_user_id = user_id
        try:
            yield
        finally:
            self._context_user_id = original_user_id

    def generate_token(self, interface_key: str) -> str:
        """生成Token：自动获取用户ID"""
        # 优先级：上下文 > 注册函数 > 异常
        if self._context_user_id:
            user_code = self._context_user_id
        elif self._user_id_getter:
            user_code = self._user_id_getter()
        else:
            raise RuntimeError("User ID source not configured")

        prefix, middle = self.INTERFACE_CONFIG[interface_key]
        original_str = f"{prefix}{middle}{user_code}"

        hash_obj = hashlib.new(self.algorithm)
        hash_obj.update(original_str.encode('utf-8'))
        return hash_obj.hexdigest().lower()
#
# if __name__ == '__main__':
#
#     Token = TokenGenerator(algorithm='md5')
#     user_id_list = [1900413066794, 1900000000118, 1900000000132]
#
#     for user_id in user_id_list:
#       user_id_str = str(user_id)
#       print(f"\n用户 {user_id} 的Token:")
#
#       # 直接传递字符串key（不再用枚举）
#       interfaces = {
#           "结算接口": "settlementTransactions"      }
#
#       with Token.user_context(user_id):
#           for name, key in interfaces.items():
#               token = Token.generate_token(key)
#               print(f"    {token}")
