$("#sales_box").hover(function(){
     $(".bar").each(function(){
        var length = $(this).find("span").html();
        $(this).find(".slideup").delay(500).animate({'height':length},
          "slow",function(){$(this).find("span").fadeIn(1000);
        });
    });
  },
  function(){
  $(".bar").each(function(){
     var length = $(this).find("span").html();
     $(this).find(".slideup").delay(500).animate({'height':0},
        "slow",function(){$(this).find("span").fadeIn(1000);
     });
  });
});
