$(function(){

    // 注册时用户名文本框失去焦点的时候
    // 获取uname,导数据库查询,判断是否存在
    function checkuname(){
            var ret = false
            var uname = $('[name=uname]').val()
            $.ajax({
                url : '/checkuname',
                type : 'get',
                data : 'uname='+uname,
                success : function(data){
                    $('.ckname').html(data)
                    if(data == '用户名已存在'){
                        ret = true
                    }
                }
            })
            return ret
        }

    $('[name=uname]').blur(function(){
        checkuname()
    })

    $('.button').click(function(){
        if(checkuname()){
            return;
        }
    })

})