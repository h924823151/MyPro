 $(function(){
            countItem()
            var imgIndex = 0;
            var timerId = setInterval(autoPlay,3000);
            function autoPlay(){
                //隐藏所有图片
                $("#banner img").each(function (){
                    $(this).css("display","none");
                })
                //下标操作
                imgIndex = ++imgIndex == $("#banner img").length ? 0 : imgIndex;
                //显示 eq(index)根据下标取元素
                $("#banner img").eq(imgIndex).css("display","block");

                //切换索引 : 修改背景色为灰色
                $("#banner li").each(function (){
                    $(this).css("background","aqua");
                })
                //图片下标对应的元素,背景色改成红色
                $("#banner li").eq(imgIndex).css("background","red");
            }
            //鼠标移入移出操作定时器
            $("#banner").bind("mouseover",function (){
                //鼠标移入,停止定时器
                clearInterval(timerId);
            })
            $("#banner").mouseout(function (){
                //鼠标移出,重启定时器
                timerId = setInterval(autoPlay,3000);
            })
            //全选
            var isChecked = false;
            $("#checkAll").click(function(){
                isChecked = !isChecked
                if(isChecked){

                    $("[name=check]").prop("checked","true");
                }else{
                    $("[name=check]").removeAttr("checked");
                }
                countItem();
            })
            //反选
            $("[name=check]").change(function(){
                var count = $("[name=check]").not("input:checked").length

                if(count == 0){
                    $("#checkAll").prop("checked","true")
                    isChecked = true;
                }else{
                    $("#checkAll").removeAttr('checked')
                    isChecked = false;
                }
                countItem();
            })

            //删除商品
            $(".g-item .action").click(function(){
                $(this).parent().remove();
                countItem();
            })
            //动态显示总价格
            function countItem(){
                var sumprice = 0
                var sumcount = 0
                $("[name=check]:checked").each(function(){
                    var priceStr = $(this).parents('.g-item').find(".price").html()
                    var price = Number(priceStr.substring(1))

                    sumprice += price
                    sumcount = $("[name=check]:checked").length

                })
                $(".submit-count span").html(sumcount)
                $(".submit-price span").html(sumprice)
            }

        })