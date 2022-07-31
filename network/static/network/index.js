document.addEventListener('DOMContentLoaded', function() {
    //edit button is pressed
    document.querySelectorAll('#edit_button').forEach(function(button){
       button.onclick = function(){
        f = document.createElement('form');
        f.id = 'edit_form';
        input_content = document.createElement('input');
        input_submit = document.createElement('input');

        input_content.id = "input_content";
        input_content.type = "text";
        input_submit.type = "submit";
        f.append(input_content);
        f.append(input_submit);

        const z = "div[value='" + button.value + "']";
        document.querySelector(z).append(f); 

        f.addEventListener('submit', () => editForm_func(f,button.value));
        
       }

    })

    document.querySelectorAll('#like_div').forEach( (theDiv) => l_liked(theDiv) )


function l_liked(theDiv){
    theDiv.innerHTML = "";
    const like_button = document.createElement('button');
    //like_button.innerHTML = "t";
    //theDiv.append(like_button);
    const post_id = theDiv.dataset.id; 
    //console.log(post_id);
    let hasLiked = false; 
    const params = {
        postId: post_id
    };
    const options = {
        method: 'POST',
        body: JSON.stringify( params )  }

    fetch('/loadLike', options)
    .then(response => response.json())
    .then(result => {
        hasLiked = result["hasLiked"];
        //console.log('test');
        //console.log(hasLiked);
        numLikes = result['numLikes'];
        console.log(numLikes);
        let num_Likes = document.createElement('p');
        num_Likes.innerHTML = `likes: ${numLikes}`;
        theDiv.append(num_Likes);

        if(hasLiked){
            //console.log("chaning to unliike");
            like_button.innerHTML = "unlike";
        }
        else{
            //console.log("changing to like");
            like_button.innerHTML = "like";
        }
        theDiv.append(like_button);
    }) 
    //console.log(hasLiked);

    like_button.addEventListener('click', () => liked(post_id, hasLiked, theDiv) );



} //endf of fdjfdka
   

function liked(post_id, has_Liked, theDiv){
    console.log(has_Liked);
    const params = {
        postId: post_id,
        hasLiked: has_Liked
    };
    const options = {
        method: 'PUT',
        body: JSON.stringify( params )  }

    fetch('/loadLike', options)
    .then(response => response.json())
    .then(result => {
        l_liked(theDiv);
        console.log(result);
        
    }) 

}
function editForm_func(form, post_id){
    let post_content = form.querySelector("#input_content").value; 
    const params = {
        postContent: post_content,
        postId: post_id
    };
    const options = {
        method: 'POST',
        body: JSON.stringify( params )  }

    fetch('/update', options)
    .then(response => response.json())
    .then(result => {
        console.log(result);
    })    
}





});  //dom content laoded one