from typing import TypedDict


class DigestModel(TypedDict):
    """摘要信息"""
    iccid: str  # 完整卡号
    card: str  # 卡号
    phone: str  # 手机号
    balance: float  # 余额
    isp: str  # 运营商
    plan: str  # 套餐
    status: str  # 网卡状态
    expired: str  # 过期时间
    total: float  # 总流量 MB
    usage: float  # 已用流量 MB
    renewal: bool # 续费
