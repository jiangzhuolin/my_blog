KindEditor.ready(function(K) {
    K.create(
     'textarea[name=content]', //页面中需要用到kindeditor编辑器的元素名称
     {
         width:1024, // 编辑器的宽
         heigth:800,    //编辑器的高
         uploadJson: '/admin/upload/kindeditor',
     });
});