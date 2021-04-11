/**
 * Created by PanJiaChen on 16/11/18.
 */

/**
 * @param {string} path
 * @returns {Boolean}
 */
export function isExternal(path) {
  return /^(https?:|mailto:|tel:)/.test(path)
}

/**
 * @param {string} str
 * @returns {Boolean}
 */
export function validUsername(str) {
  const valid_map = ['admin', 'editor']
  return valid_map.indexOf(str.trim()) >= 0
}

export function validPhone(phone) {
  if (!(/^1[3|4|5|7|8]\d{9}$/.test(phone))) {
    return false
  } else {
    return true
  }
}

export function validEmail(email) {
  if (!(/^\w+((.\w+)|(-\w+))@[A-Za-z0-9]+((.|-)[A-Za-z0-9]+).[A-Za-z0-9]+$/.test(email))) {
    return false
  } else {
    return true
  }
}

export function validIdCard(idCard) {
  if (typeof idCard !== 'string') {
    return {
      code: -1,
      msg: '为了避免javascript数值范围误差，idCard 必须是字符串'
    }
  }
  const idcard_patter = /^[1-9][0-9]{5}([1][9][0-9]{2}|[2][0][0|1][0-9])([0][1-9]|[1][0|1|2])([0][1-9]|[1|2][0-9]|[3][0|1])[0-9]{3}([0-9]|[X])$/
  // 判断格式是否正确
  const format = idcard_patter.test(idCard)
  if (!format) {
    return {
      code: -1,
      msg: '身份证号码格式错误'
    }
  }
  // 加权因子
  const weight_factor = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
  // 校验码
  const check_code = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
  const last = idCard[17]// 最后一位
  const seventeen = idCard.substring(0, 17)
  // ISO 7064:1983.MOD 11-2
  // 判断最后一位校验码是否正确
  const arr = seventeen.split('')
  const len = arr.length
  let num = 0
  for (let i = 0; i < len; i++) {
    num += arr[i] * weight_factor[i]
  }
  // 获取余数
  const resisue = num % 11
  const last_no = check_code[resisue]
  // 返回验证结果，校验码和格式同时正确才算是合法的身份证号码
  const result = last === last_no
  return {
    code: result ? 1 : -1,
    msg: !result ? '身份证号码格式错误' : ''
  }
}
