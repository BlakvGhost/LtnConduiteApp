$(document).ready(function() {
  function ajaxRequest(mainContain,labelToWrite) {
    function check(self) {
      $.ajax({url:'/ifExist/',data:$(self).serialize(),success:function(e){if (!e){$(self).addClass('is-invalid');$('#submit_vote').hide(); }else{$(self).removeClass('is-invalid');$('#submit_vote').show()};}})
    }
    $(mainContain).each(function(px,classE) {
      $(classE).keyup(function() {
        let contains = $(labelToWrite).find('li');
        if ($(this).val().length == 0){
          $(contains).detach();
        }else {
          $(contains).detach();
          $.ajax({url:'/checkClass/',data:$(this).serialize(),success:function(e){$(e).each(function(px,list){let li = document.createElement('li');$(li).addClass('list-group-item list-group-item-action');$(li).text(list);$(labelToWrite).append(li);$(li).click(function(){$(mainContain).val($(this).text());check(mainContain);$(labelToWrite).find('li').detach();})})}})
        }
      });
      $(classE).change(function(){
        check($(this));
      })
    })
  }
  $('.gener').click(function () {
    let id = Math.ceil(Math.random()*277878377777);
    $('#id_id').val('ltn'+id);
    $('#id_mdp').val('password'+id);
  })
  $('.delete_btn').each(function (px,btn){
    $(btn).click(function(){
      $('.toDelete').text($(this).data('name'));
      $('#id_hid').val($(this).data('id'));
      $('#id_active').val('#'+ $(this).data('user-id'))
    })
});
$('.edit_btn').each(function (px,btn){
    $(btn).click(function(){
      $('#id_id,#id_idD').val($(this).data('user-id'));
      $('#id_nom').val($(this).data('nom'));
      $('#id_user').val($(this).data('id'));
      $('#id_prenom').val($(this).data('prenom'));
      $('.teaUserName').text($(this).data('name'));
    });
  })
let content = $('.vote-item').eq(0).html();
$('.addSpecification').click(function (){
    let specificItem = document.createElement('div');
    $(specificItem).addClass("input-group input-group-lg my-3 vote-item");
    let id = 'detail-'+Math.round(Math.random()*667);
    specificItem.id = id;
    $(specificItem).html(content);
    $(specificItem).find('.remove-item').data('remove',`#${id}`)
    $('.vote-label').append(specificItem);
    $('.remove-item').each(function (e,item){$(item).click(function(){$($(this).data('remove')).detach();})});
    ajaxRequest($(specificItem).find('#id_classe'),$(specificItem).find('#label_checkClass'));
});
ajaxRequest('#id_classe','#label_checkClass');
})
