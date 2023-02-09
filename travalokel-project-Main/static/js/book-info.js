var d = new Date();
var strDate = d.getFullYear() + "/" + (d.getMonth()+1) + "/" + d.getDate();

$(document).ready(function () {
    const params = (new URL(document.location)).searchParams
    const id = params.get('flight_ID')
    $.ajax({
        url:  '/flight/detail/' + id,
        type:  'get',
        dataType:  'json',
        success: function  (data) {
            console.log(data)
            $('#info-departure').html(data.paths.departure);
            $('#info-destination').html(data.paths.destination);
            $('#info-departure_date').html(data.flight.departure_date);
            $('#airline').html(data.flight.airline);
            $('#info-departure_time').html(data.flight.departure_time);
            $('#info-departure2').html(data.paths.departure);
            $('#info-duration').html(data.flight.duration);
            $('#info-arrival_time').html(data.flight.arrival_time);
            $('#info-destination2').html(data.paths.destination);

            $('#flight_id').val(data.flight.flight_id)
            $('#seat_class').val(data.flight_detail.seat_class)
            $('#total_amount').val(data.flight_detail.price)
            $('#booking_date').val(strDate)
            $('#departure_date').val(data.flight.departure_date)

        },
        error: function(error){
            console("Error ${error}")
        }
    })

})

