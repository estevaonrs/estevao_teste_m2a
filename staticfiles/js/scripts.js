$(document).ready(function() {
    $('.tank-item').click(function() {
        var tankId = $(this).data('id');
        $.ajax({
            url: loadPumpsUrl,
            type: 'POST',
            data: {
                'tank_id': tankId,
                'csrfmiddlewaretoken': '{{ csrf_token }}'
            },
            success: function(pumps) {
                $('#pumpList').empty();
                pumps.forEach(function(pump) {
                    $('#pumpList').append('<button type="button" class="list-group-item list-group-item-action pump-item" data-id="' + pump.id + '">' + pump.name + '</button>');
                });
                $('#step1').hide();
                $('#step2').show();
            }
        });
    });

    $(document).on('click', '.pump-item', function() {
        var pumpId = $(this).data('id');
        $('#selectedPump').val(pumpId);
        $('#step2').hide();
        $('#step3').show();
    });

    $('#refuelForm').submit(function(event) {
        event.preventDefault();
    
        var amountInput = $('#amount');
        var amountValue = amountInput.val().replace(/\./g, '').replace(',', '.').trim();
        amountInput.val(amountValue);

        var litersInput = $('#liters');
        var litersValue = litersInput.val().replace(/\./g, '').replace(',', '.').trim();
        litersInput.val(litersValue);
    
        $.ajax({
            url: saveRefuelUrl,
            type: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                if (response.status === 'success') {
                    $('#refuelModal').modal('hide');
                    $('#successModal').modal('show');
                } else {
                    alert('Erro ao registrar o abastecimento.');
                }
            },
            error: function(xhr, errmsg, err) {
                alert('Erro ao registrar o abastecimento. Por favor, tente novamente.');
            }
        });
    });

    $('#successModal').on('hidden.bs.modal', function (e) {
        location.reload(); 
    });

    $('#reportForm').submit(function(event) {
        event.preventDefault();
        var startDate = $('#startDate').val();
        var endDate = $('#endDate').val();
        var url = downloadReportUrl + '?start_date=' + startDate + '&end_date=' + endDate;
        window.open(url, '_blank');
        $('#reportModal').modal('hide');
    });
});