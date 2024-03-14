
// function NewPost(){

//     return(
//         <div>This is a new post...</div>
//     );
// }

// function App(){
//     return(
//         //JSX code or javascript xml
//         <div><NewPost /></div>
//     );
// }

// ReactDOM.render(<App />, document.querySelector("#app"));

document.addEventListener("DOMContentLoaded", () => {
const post = document.querySelector("#btn-post");
const postForm = document.querySelector("#postForm");
const likeForm = document.querySelector("#likes");
const likeBtn = document.querySelector("#like-btn");
const unlikeBtn = document.querySelector("#unlike-Btn");


//check if a new post is submitted and if the user did not type anything.
postForm.addEventListener('submit', (event) => {
    const error = document.querySelector("#posts-error");
    const posts = document.querySelector("#posts").value;
    const trimmedValue = posts.replace(/\s+/g, '');
    if (trimmedValue === "")
    {
        
        event.preventDefault();
        error.innerHTML = "You have to write a post!";
        console.log(error.innerHTML);
        error.style.color = "red";
    }
    else{
        error.style.display = 'none';
    }
    //return false;
});

likeForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const formData = new FormData(likeForm);
    const id = formData.get('post_id');
    const url = `/posts/${id}/`;
    fetch(url, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log(data.likes);
            likeBtn.innerHTML = `Likes: ${data.likes}`;
            return data.likes;
        }
        else{
            console.log(data.error);
        }
    })
    .catch(error => {
        console.log(error);
    });

});

});