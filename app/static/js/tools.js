//获取两个日期字符串相隔的天数
function getDays(date1, date2) {//date1:小日期   date2:大日期
    var sdate = new Date(date1);
    var now = new Date(date2);
    var days = now.getTime() - sdate.getTime();
    var day = parseInt(days / (1000 * 60 * 60 * 24));
    return day;
}

function getFloatDays(date1, date2) {
    var sdate = new Date(date1);
    var now = new Date(date2);
    var days = now.getTime() - sdate.getTime();
    var day = parseFloat(days / (1000 * 60 * 60 * 24)).toFixed(1);
    return day;
}

//根据出生日期计算年龄，精确到小数
function getAge(strBirth) {
    var now = new Date()
    var birth = new Date(strBirth)
    var birthY = birth.getFullYear()
    var birthM = birth.getMonth() + 1
    var birthD = birth.getDate()
    var currY = now.getFullYear()
    var currM = now.getMonth() + 1
    var currD = now.getDate()
    var currBirth = currY + '-' + birthM + '-' + birthD
    var nextBirth = (currY + 1) + '-' + birthM + '-' + birthD
    var lastBirth = (currY - 1) + '-' + birthM + '-' + birthD
    var strNow = currY + '-' + currM + '-' + currD
    if (new Date(currBirth) < new Date(strNow)) {
        var ageInt = currY - birthY
        var currDay = getDays(currBirth, strNow)
        var allDay = getDays(currBirth, nextBirth)
        var ageFloat = currDay / allDay
        var age = ageInt + ageFloat
    } else if (new Date(currBirth) > new Date(strNow)) {
        var ageInt = currY - birthY - 1
        var currDay = getDays(lastBirth, strNow)
        var allDay = getDays(lastBirth, currBirth)
        var ageFloat = currDay / allDay
        var age = ageInt + ageFloat
    } else {
        var age = currY - birthY
    }
    return age.toFixed(1)
}