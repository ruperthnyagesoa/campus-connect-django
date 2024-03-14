document.addEventListener("DOMContentLoaded", () => {
    
    let isSuccess = false;
    const followBtn = document.querySelector("#follow-id-btn");
    const unfollowBtn = document.querySelector("#unfollow-id-btn");
    const followForm = document.querySelector("#following");
    const unfollowForm = document.querySelector("#unfollow");
    const unfollowDiv = document.querySelector("#unfollow-div");
    const followDiv = document.querySelector("#follow-div");


    isSuccess = followings;
    //followings = isSuccess;
    console.log('following: ', followings);
    console.log('not following: ', !followings);
    console.log('isSuccess: ', isSuccess);
    //console.log('is same profile: ', isSameUser);
   
    if (followDiv || unfollowDiv){
    if (followings) {
        followDiv.style.display = 'none';
        //if (unfollowBtn){
        unfollowDiv.style.display = 'inline-block';
        //}
    
    } else {
        
        followDiv.style.display = 'inline-block';
        unfollowDiv.style.display = 'none';

    }
}
    console.log('following 2: ', followings);

    //this check is done to fix the error of not seeing the follow or unfollow forms 
    if (followForm || unfollowForm){

    followForm.addEventListener('submit', (event) => {
      event.preventDefault();
    
       const formData = new FormData(followForm);
       const id = formData.get('id');
       const url = `/profile/${id}/`;
      //TODO: Update the views.py to ensure it returns an appropriate json response to make this work!
       try {
        fetch(url, {
          method: 'POST',
          body: formData
        })
          .then(response => response.json())
          .then(data => {
            if (data.success) {
              
              followDiv.style.display = 'none';
              unfollowDiv.style.display = 'inline-block';
              return followings = true;
              
              console.log('following 3: ', followings);
              console.log(data.posts);
            } else {
              console.log(data.error);
              followings = false;
              isSuccess = false;
            }
          });
      } catch (error) {
        console.error('Follow user request failed:', error);
        isSuccess = false;
      }
    });

    console.log(unfollowForm);
    unfollowForm.addEventListener('submit', (event) => {
        event.preventDefault();

         const formData = new FormData(unfollowForm);
         const id = formData.get('id');
        try {
         fetch(`/unfollow/${id}/`, {
            method: 'POST',
            body: formData
            // headers: {
            //     'X-CSRFToken': csrf_token,
            //     'Content-Type': 'application/json'
            // }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                
                followDiv.style.display = 'inline-block';
                unfollowDiv.style.display = 'none';
                return followings = false;
                isSuccess = false;
                
            } else {
                console.error(data.error);
                followings = true;
                isSuccess = true;
            }
        });
    }
    catch (error) {
        console.error('Follow user request failed:', error);
        isSuccess = false;
        followings = false;
      }
          
      });
    }
    //}


});