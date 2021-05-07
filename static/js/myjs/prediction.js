$(document).ready(function () {
  // timeseries begin and year
  let currentURL = $(location).attr('pathname');
  if (currentURL != '/prediction') {
    return false;
  }
  $(".trainBegin").change(function () {
    var val = $(this).val();
    var min = $(this).attr("min");
    var max = $(this).attr("max");
    // console.log(min,' ',max);
    var portion = (val - min) / (max - min);
    $(".indicator_begin_train").text(val);
    $(".indicator_begin_train").css("left", portion * ($(".begin").width() - 18));
    // check time
    var trainBegin = $(".trainBegin").val();
    var trainEnd = $(".trainEnd").val();
    var testEnd = $(".testEnd").val();
  });
  // end year
  $(".trainEnd").change(function () {
    var val = $(this).val();
    var min = $(this).attr("min");
    var max = $(this).attr("max");
    var portion = (val - min) / (max - min);
    $(".indicator_end_train").text(val);
    $(".indicator_end_train").css("left", portion * ($(".end").width() - 18));
    var trainBegin = $(".trainBegin").val();
    var trainEnd = $(".trainEnd").val();
    var testEnd = $(".testEnd").val();
  });

  $(".testEnd").change(function () {
    var val = $(this).val();
    var min = $(this).attr("min");
    var max = $(this).attr("max");
    var portion = (val - min) / (max - min);
    $(".indicator_end_test").text(val);
    $(".indicator_end_test").css("left", portion * ($(".end").width() - 18));
    var trainBegin = $(".trainBegin").val();
    var trainEnd = $(".trainEnd").val();
    var testEnd = $(".testEnd").val();
  });

  // check nhieu loai benh
  var disease_array = [];
  var globalDisease=''
  $(".check_disease").click(function () {
    var begin = $(".begin").val();
    var end = $(".end").val();

    if (this.checked) {
      //disease_array.push(this.value);
      globalDisease=this.value;
    } else {
      //disease_array.pop(this.value);
    }
  });


  var globalProvince=''
  $(".check_province").click(function () {
    var begin = $(".begin").val();
    var end = $(".end").val();

    if (this.checked) {
      //disease_array.push(this.value);
      globalProvince=this.value;
    } else {
      //disease_array.pop(this.value);
    }
  });
  // check nhieu yeu to
  var climate_array = [];
  $(".check_climate").click(function () {
    var begin = $(".begin").val();
    var end = $(".end").val();
    if (this.checked) {
      climate_array.push(this.value);
    } else {
      climate_array.pop(this.value);
    }
  });
  // on click disease
  // get region climate

   $(".predict_button").click(function () {
     $(`#prediction_${0}`).remove();
     let climate_array_string = climate_array.join("-");
     var disease = globalDisease;
     var province = globalProvince;
     var trainBegin = $(".trainBegin").val();
     var trainEnd = $(".trainEnd").val();
     var testEnd = $(".testEnd").val();
     if(globalDisease=='' || globalProvince==''){
       window.alert("Please Select a disease and province -  For multivariate model also select Climate Factors");
     } else if (!(trainBegin<trainEnd && trainEnd<testEnd)) {
       window.alert("Invalid Year Selection")
       $(".trainBegin").val(1997);
       $(".indicator_begin_train").text(1997);
       $(".trainEnd").val(2008);
       $(".indicator_end_train").text(2008);
       $(".testEnd").val(2016);
       $(".indicator_end_test").text(2016);
     }
     else {
       window.alert("Model training - Do not refresh Page")
       $.ajax({
         url: "/get_prediction",
         type: "GET",
         contentType: "application/json;charset=UTF-8",
         data: {
           name: climate_array_string,
           disease: disease,
           province: province,
           trainBegin: trainBegin,
           trainEnd: trainEnd,
           testEnd: testEnd
         },
         dataType: "json",
         success: function (data) {
           Plotly.newPlot(`monthly_cases`, data, {});
           // monthly number of influenza incidence
           $(`#title_monthly_cases_${0}`).html(`Projected Monthly number of cases of ${name.split('_').join('  ')}  in Viet Nam from ${begin}-${end}`);
         }
       });
       var html = '';
       html += `<div class="product-sales-area mg-tb-30" id=prediction_${0}>
        <div class="container-fluid">
            <!-- show chart climate in here  -->
            <div class="row">
                <!-- begin col 1  -->
                <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
                    <div class="product-sales-chart">
                        <div class="portlet-title">
                            <div class="row">
                                <div class="col-lg-6 col-md-6 col-sm-6 col-xs-12">
                                    <div class="caption pro-sl-hd">
                                        <span class="caption-subject" id=title_monthly_cases_${0}><b></b></span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <!-- chart in here -->
                        <div id="monthly_cases" class="monthly_cases"
                            style="height: auto;width:auto"></div>
                    </div>
                </div >
            </div>
        </div>
    </div>`
       $(".disease_chart").append(html);
       $('.title_home').html(`Predicted ${disease} Cases in ${province}`)
     }
  });


  // title home default
  title_home(1997, 2016);
  function title_home(begin, end) {
    $('.title_home').html(`Predict Disease Cases in Vietnam`)
  }

});
