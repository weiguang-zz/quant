/**
 * Created by zhangzheng on 16/9/20.
 */

function choose(){
    data={
        'fastkperiod':$("input[name=fastkperiod]").value,
        'slowkperiod':$("input[name=slowkperiod]").value,
        'slowdperiod':$("input[name=slowdperiod]").value
    };

    $.ajax({
        type: 'POST',
        url: "/index" ,
        data: data ,
        success: function(){
            alert("haha")
        }

    })



}