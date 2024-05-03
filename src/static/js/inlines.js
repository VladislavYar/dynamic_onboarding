let title;

/**
 * Удаляет choice-поля, кроме первого.
 * 
 */
function removeChoices() {
    const re = new RegExp('^choices-[1-9]{1}[0-9]*$');
    if (re.test($(this).attr('id'))) {
        $(this).remove();
    }
}

/**
 * Скрывает элементы добавлени и удаления поля для ввода при старте.
 * 
 */
function startHideAddDelete() {
    title = $('th.column-name').html();
    let text = $('#id_field_type').find('option:selected').text();
    let text_readonly = $('div.readonly').text();
    console.log(text_readonly);
    if (
        text.toLowerCase().substr(-5, 5).indexOf('true') < 0 &&
        text_readonly.toLowerCase().substr(-5, 5).indexOf('true') < 0
    ) {
        $('th.column-name').html('');
        $('.original').hide();
        setTimeout(
            '$(".add-row").hide();' +
            '$("#id_choices-0-name").hide();' + 
            '$("#id_choices-0-name").attr("value", "noname");' + 
            '$(".inline-deletelink").hide();' +
            '$(\'[id^="choices-"]\').each(removeChoices);', 1
        );
    }
}


/**
 * Скрывает элементы добавлени и удаления поля для ввода.
 * 
 */
function hideAddDelete() {
    $('.add-row').hide();
    $('.inline-deletelink').hide();
    $('#id_choices-0-name').hide();
    $('.original').hide();
    $("th.column-name").html('');
    $('#id_choices-0-name').attr('value', 'noname');
    $('#id_choices-TOTAL_FORMS').attr('value', '1');
    $('[id^="choices-"]').each(removeChoices);

}

/**
 * Выводит элементы добавления и удаления поля для ввода.
 * 
 */
function showAddDelete() {
    $('.add-row').show();
    $('.original').show();
    $('.inline-deletelink').show();
    $('#id_choices-0-name').show();
    $("th.column-name").html(title);
    $('#id_choices-0-name').attr('value', '');
}

/**
 * Проверяет выбранное значение на множественность.
 * 
 */
function changeOption() {
    let text = $(this).find('option:selected').text();
    if (text.toLowerCase().substr(-5, 5).indexOf('true') >= 0) {
        showAddDelete();
        return;
    }
    hideAddDelete();
}

function main() {
    startHideAddDelete();
    $('#id_field_type').change(changeOption);
}

$(main);