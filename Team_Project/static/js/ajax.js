function AjaxSendAppid() {
    $.ajax({
        url: searchappid,
        type: 'POST',
        data: {'appid': $('#appid').val(), 'csrfmiddlewaretoken': csrf_token},
        success: function (data) {
            console.log(data);
            if (data > 0) {
                $('#searchModal').modal('show')
                location.href = '/game/' + data
            } else {
                $('#appid').addClass('is-invalid')
                $('.input-group').addClass('was-validated')
                $('.invalid-feedback').text('Please enter appid number!')
            }

        }
    })
}

function AjaxSendSearch() {
    $.ajax({
        url: search,
        type: 'POST',
        data: {'search': $('#search').val(), 'csrfmiddlewaretoken': csrf_token},
        success: function (data) {
            console.log(data);
            if (data == 'Wrong') {
                $('#searchModal').modal('hide')
                $('#search').addClass('is-invalid')
                $('#navbarSearch').addClass('was-validated')
                $('.invalid-feedback').text('Please enter something!')
            } else {
                $('#searchModal').modal('show')
                location.href = '/search/' + data
            }

        }
    })
}

function AjaxLike() {
    $.ajax({
        url: url_like,
        type: 'POST',
        data: {'appid': appid, 'csrfmiddlewaretoken': csrf_token},
        success: function (data) {
            console.log(data);
            if (data === 'Like') {
                $('#btn-like').attr('class', 'btn btn-outline-danger')
                $('#btn-like').text('Dislike..')
            } else if (data === 'Dislike') {
                $('#btn-like').attr('class', 'btn btn-outline-primary')
                $('#btn-like').text('Like!')
            }
        }
    })
}

function AjaxComment() {
    if ($('#commentArea').val() === "") {
        $('#commentArea').addClass('is-invalid')
        $('.form-group').addClass('was-validated')
        $('.invalid-feedback').text('Please enter something!')
    } else {
        var comment = $('#commentArea').val()
        var date = new Date();
        var html = "<div class=\"card\" style=\"margin-top: 20px; text-align: left\">\n" +
            "                        <div class=\"card-header\" style=\"height: 30px; line-height: 0px\">\n" +
            user_name +
            "                        </div>\n" +
            "                        <div class=\"card-body\">\n" +
            "                            <blockquote class=\"blockquote mb-0\">\n" +
            "                                <p>" + comment + "</p>\n" +
            "                                <footer class=\"blockquote-footer\">Commented at " + date.toLocaleString() + " </footer>\n" +
            "                            </blockquote>\n" +
            "                        </div>\n" +
            "                    </div>"
        $.ajax({
            url: url_comment,
            type: 'POST',
            data: {
                'appid': appid,
                'comment': comment,
                'csrfmiddlewaretoken': csrf_token
            },
            success: function (data) {
                console.log(data);
                if (data === 'OK') {
                    $('#user-comments').prepend(html)
                } else if (data === 'ALREADY COMMENT TWICE') {
                    $('#user-comments').prepend(html)
                    $('#commentArea').remove()
                    $('#btn-comment').remove()
                    $('.form-group').after("<a type=\"button\" class=\"btn btn-outline-primary btn-lg btn-block disabled\"\n" +
                        "                       style=\"height: 30px; line-height: 10px; margin-top: -10px\">You've already commented twice!\n" +
                        "                    </a>")
                } else {
                    $('#commentArea').remove()
                    $('#btn-comment').remove()
                    $('.form-group').after("<a type=\"button\" class=\"btn btn-outline-primary btn-lg btn-block disabled\"\n" +
                        "                       style=\"height: 30px; line-height: 10px; margin-top: -10px\">You've already commented twice!\n" +
                        "                    </a>")

                }

            }
        })
    }

}