/**
 * Created by Zander on 2017-05-01.
 */
$(function () {
    $('.navbar-toggle-sidebar').click(function () {
        $('.navbar-nav').toggleClass('slide-in');
        $('.side-body').toggleClass('body-slide-in');
        $('#search').removeClass('in').addClass('collapse').slideUp(200);
    });

    $('#search-trigger').click(function () {
        $('.navbar-nav').removeClass('slide-in');
        $('.side-body').removeClass('body-slide-in');
        $('.search-input').focus();
    });
});
// 删除导航
function delMenu(url) {
    $('#delMenuClick').click(function () {
        window.location.href = url;
    });
    $('#delMenuModal').modal();
}

function getMenu_info(url) {
    $.ajax({
        url : url,
        method : 'get',
        dataType : 'json',
        success : function (menuinfo) {
            $('#id').val(menuinfo.id);
            $('#menuname').val(menuinfo.menuname);
            $('#visibled').attr('checked',menuinfo.visibled)
        }
    });
    $('#editmodel').modal();

}