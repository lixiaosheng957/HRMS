export function compareDate(d1, d2) {
  const date1 = new Date(Date.parse(d1))
  const date2 = new Date(Date.parse(d2))
  return date1 > date2
}

export function today() {
  const now = new Date()
  const year = now.getFullYear()
  let month = now.getMonth() + 1
  let day = now.getDate()
  if (month >= 1 && month <= 9) {
    month = '0' + month
  }
  if (day >= 0 && day <= 9) {
    day = '0' + day
  }
  return year + '-' + month + '-' + day
}
