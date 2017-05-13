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


//删除分类
function delCategory(url) {
    $('#delCategoryCli').click(function () {
        window.location.href = url;
    });
    $('#delCategoryModal').modal();
}

// 删除导航
function delMenu(url) {
    $('#delMenuClick').click(function () {
        window.location.href = url;
    });
    $('#delMenuModal').modal();
}

// 删除文章
function delPost(url) {
    $('#delPostCli').click(function () {
        window.location.href = url;
    });
    $('#delPostModal').modal();

}
//修改分类
function getCategory_info(url) {
    $.ajax({
        url : url,
        method : 'get',
        dataType : 'json',
        success : function (categoryinfo) {
            $('#id').val(categoryinfo.id);
            $('#categoryname').val(categoryinfo.categoryname);
            $('#menuselect').val(categoryinfo.menuid)
        }
    });
    $('#editCategoryModal').modal();
}

// 修改导航
function getMenu_info(url) {
    $.ajax({
        url: url,
        method: 'get',
        dataType: 'json',
        success: function (menuinfo) {
            $('#id').val(menuinfo.id);
            $('#menuname').val(menuinfo.menuname);
            $('#visibled').attr('checked', menuinfo.visibled)
        }
    });
    $('#editmodel').modal();

}