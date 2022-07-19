# 身份验证
hardcoded_token = "this_is_a_token"

# 是否禁用身份验证
disable_verification = False


def auth_by_token(token: str) -> bool:
    """
    检验这个token是否正确。  todo: 目前token是硬编码的，以后最好能放到数据库里

    :param token: str
    :return: bool
    """
    if disable_verification:
        return True
    return token == hardcoded_token
