$(document).ready( function () {
    $('#btnPrint').click(function () {
        if ($('#txt_ticketID').val() == '') {
            alert ('ยังไม่ระบุุ ticket_id');
            return false;
        }
        window.open('/ticket/report/' + $('#txt_ticketID').val());
    });
});