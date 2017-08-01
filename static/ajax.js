/**
 * Created by Artur on 27.07.2017.
 */
$.ajax({
    url: '/ajax/',
    type: 'POST',
    data:{post_id: 12,text:'mkmkmlmlkm'},
}).success(function(data){
    if (data.status=='ok'){
        console.log(data.commet_id);
    }
}).error(function(){
    console.log('http error')
});