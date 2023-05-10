import { processUploadCoverPhoto, processUploadProfilePicture } from "./profile/images.js"
import { processNewPost } from "./profile/newPost.js";
import { processPostLoading } from "./profile/posts.js";
import { processFriending } from "./friending.js"
import { processSectionFriends } from "./profile/sectionFriends.js"
import { pluralizeWord } from "./helper/helper.js"

console.log(window.CSRF_TOKEN)

export function processProfile(secondUserProfileUrl) {
    /*
    pr.second_user_id

    pr.posts_index_url
    pr.posts_create_url
    pr.upload_cover_photo_url
    pr.upload_profile_picture_url
    pr.friending_index_url
    pr.friending_requests_url

    pr.cover_url
    pr.profile_url_round
    pr.first_name
    pr.last_name
    pr.num_friends
    pr.main_friending_state
*/

    function processSelectAndContentAll(pr) {
        function processSelectAndContent(selectParent, selectContentParent) {
            let selectLinks = selectParent.children
            let selectContentBlocks = selectContentParent.children
            Array.from(selectLinks).forEach((link, i) => {
                if (Array.from(link.classList).includes('home-required')) {
                    if (window.currentUserId != pr.second_user_id) {
                        link.style.display = 'none'
                    }
                }
                link.addEventListener('click', e => {
                    e.preventDefault()
                    e.stopPropagation()
                    for (let j = 0; j < selectLinks.length; j++) {
                        if (j == i) {
                            selectLinks[j].classList.add('active')
                            selectContentBlocks[j].style.display = 'flex'
                        } else {
                            selectLinks[j].classList.remove('active')
                            selectContentBlocks[j].style.display = 'none'
                        }
                    }
                })
            })
            // auto click
            if (Array.from(selectLinks[0].classList).includes('click')) {
                selectLinks[0].click()
            }
        }

        let allSelectParents = document.querySelectorAll(`.myselect`)
        let allSelectContentParents = document.querySelectorAll(`.myselect-content`)
        for (let i = 0; i < allSelectParents.length; i++) {
            processSelectAndContent(allSelectParents[i], allSelectContentParents[i])
        }
    }
    function processHomeProfile(pr) {
        let fullname = document.querySelector(`#info .full-name`)
        fullname.innerText = `${pr.first_name} ${pr.last_name}`
        let numFriends = document.querySelector(`#info .num-friends`)
        let numFriend = parseInt(pr.num_friends)
        numFriends.innerHTML = numFriend + ' ' + pluralizeWord('friend', 'friends', numFriend)
        let profilePicture = document.querySelector('#profile-picture>img');
        profilePicture.src = pr.profile_url_round
        let coverPhoto = document.querySelector('#cover-photo>img');
        coverPhoto.src = pr.cover_url
        let coverPhotoHome = document.querySelector(`#cover-photo .dropdown`)
        let profilePictureHome = document.querySelector(`#profile-picture .dropdown`)
        let newPostHome = document.querySelector(`#whole-new-post`)
        let homeSections = [coverPhotoHome, profilePictureHome, newPostHome]
        if (window.currentUserId == pr.second_user_id) {
            processUploadCoverPhoto(pr.upload_cover_photo_url);
            processUploadProfilePicture(pr.upload_profile_picture_url);
            processNewPost(pr.posts_create_url);
            homeSections.forEach(s => {
                s.style.display = 'block'
            })
        } else {
            homeSections.forEach(s => {
                s.style.display = 'none'
            })
        }
    }
    function process(pr) {
        processHomeProfile(pr)
        processSelectAndContentAll(pr)
        processFriending('mainFriending', pr.main_friending_state, true, null);
        // append
        processSectionFriends(pr.friending_index_url, pr.friending_requests_url)
        processPostLoading(pr.posts_index_url, pr.main_friending_state);
    }

    axios.get(secondUserProfileUrl, {
        params: {}
    })
        .then(function (response) {
            if (response.data.error) {
                console.log('ERROR!')
                console.log(response.data.error)
                return
            }
            console.log('SUCCESS!!');
            console.log(response.data.profile)
            process(response.data.profile)
        })
        .catch(function (err) {
            console.log('FAILURE!!');
            console.log(err)
        });


}