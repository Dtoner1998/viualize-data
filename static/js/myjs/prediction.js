$(document).ready(function () {
  // timeseries begin and year
  let currentURL = $(location).attr('pathname');
  if (currentURL != '/prediction') {
    return false;
  }
  $(".begin").change(function () {
    var val = $(this).val();
    var min = $(this).attr("min");
    var max = $(this).attr("max");
    // console.log(min,' ',max);
    var portion = (val - min) / (max - min);
    $(".indicator_begin").text(val);
    $(".indicator_begin").css("left", portion * ($(".begin").width() - 18));
    // check time
    var begin = $(".begin").val();
    var end = $(".end").val();
    if (begin > end) {
      $.confirm({
        title: 'Confirm',
        content: 'Please choose begin year bigger than or equal end year!',
        iconClose: true,
        buttons: {
          ok: {
            btnClass: 'btn-primay',
            action: function () {
              $(".begin").val(min);
              $(".indicator_begin").text(min);
              title_home(min, end);
            }
          },
        }
      });
      return false;
    }
    title_home(begin, end);
    get_data_home();
  });
  // end year
  $(".end").change(function () {
    var val = $(this).val();
    var min = $(this).attr("min");
    var max = $(this).attr("max");
    var portion = (val - min) / (max - min);
    $(".indicator_end").text(val);
    $(".indicator_end").css("left", portion * ($(".end").width() - 18));
    var begin = $(".begin").val();
    var end = $(".end").val();
    if (begin > end) {
      $.confirm({
        title: 'Confirm',
        content: 'Please choose begin year bigger than or equal end year!',
        iconClose: true,
        buttons: {
          ok: {
            btnClass: 'btn-primay',
            action: function () {
              $(".begin").val(min);
              $(".indicator_begin").text(min);
              console(min);
              title_home(min, end);
            }
          },
        }
      });
      return false;
    }
    title_home(begin, end);

    get_data_home();
  });
  // check nhieu loai benh
  var disease_array = [];
  $(".check_disease").click(function () {
    var begin = $(".begin").val();
    var end = $(".end").val();

    if (this.checked) {
      disease_array.push(this.value);
    } else {
      disease_array.pop(this.value);
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
     let climate_array_string = climate_array.join("+");
     $.ajax({
      url: "/get_prediction",
      type: "GET",
      contentType: "application/json;charset=UTF-8",
      data: {
        name: climate_array_string,
        disease : 'dengue_fever'
      },
      dataType: "json",
      success: function (data) {
        Plotly.newPlot(`monthly_trendline_cases_${order}`, data, {});
        // monthly number of influenza incidence
        $(`#title_monthly_trendline_cases_home_${order}`).html(`Monthly number of cases of ${name.split('_').join('  ')}  in Viet Nam from ${begin}-${end}`);
      },
    });
  });


  // title home default
  title_home(1997, 2019);
  function title_home(begin, end) {
    $('.title_home').html(`Summary Data In Viet Nam From ${begin}-${end}`)
  }

});
