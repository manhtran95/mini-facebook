
import { pluralizeWord } from "../helper/helper.js"

export function processFriending(friendingClass, friendingState, isMain, urls) {
    function displayFriendingWithState(state) {
        // DISPLAY the correct state block
        let nonFriendNode = document.querySelector(`.${friendingClass} .friending-non-friend`)
        let requestSentNode = document.querySelector(`.${friendingClass} .friending-request-sent`)
        let requestReceivedNode = document.querySelector(`.${friendingClass} .friending-request-received`)
        let friendNode = document.querySelector(`.${friendingClass} .friending-friend`)
        let nodes = {
            'NON-FRIEND': nonFriendNode,
            'REQUEST-SENT': requestSentNode,
            'REQUEST-RECEIVED': requestReceivedNode,
            'FRIEND': friendNode
        }
        for (const [nodeState, node] of Object.entries(nodes)) {
            if (nodeState == state) {
                node.style.display = 'block'
            } else {
                node.style.display = 'none'
            }
        }
    }

    // make AJAX calls to server for 5 actions
    function processFormButtons() {
        // process form url
        if (urls) {
            let formAddFriend = document.querySelector(`.${friendingClass} form[name='add-friend']`)
            let formCancelRequest = document.querySelector(`.${friendingClass} form[name='cancel-request']`)
            let formConfirmRequest = document.querySelector(`.${friendingClass} form[name='confirm-request']`)
            let formDeleteRequest = document.querySelector(`.${friendingClass} form[name='delete-request']`)
            let formUnfriend = document.querySelector(`.${friendingClass} form[name='unfriend']`)

            formAddFriend.action = urls.add_friend
            formCancelRequest.action = urls.cancel_request
            formConfirmRequest.action = urls.confirm_request
            formDeleteRequest.action = urls.delete_request
            formUnfriend.action = urls.unfriend
        }

        let formButtons = document.querySelectorAll(`.${friendingClass} form button`)
        formButtons.forEach(formButton => {
            let form = formButton.parentNode;
            formButton.addEventListener('click', function (e) {
                e.preventDefault()
                e.stopPropagation()
                formButton.disabled = true

                axios.post(form.action, {
                    csrfmiddlewaretoken: window.CSRF_TOKEN
                }, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                })
                    .then(function (response) {
                        formButton.disabled = false
                        console.log('SUCCESS!');
                        console.log(response.data);
                        if (response.data.error) {
                            return
                        }
                        // next state
                        displayFriendingWithState(response.data.state)
                    })
                    .catch(function (error) {
                        console.log('ERROR!');
                        console.log(error);
                    });
            })
        })
    }



    if (isMain) {
        // remove old main Friending
        let oldMainFriending = document.querySelector('.mainFriending')
        if (oldMainFriending) {
            oldMainFriending.parentNode.removeChild(oldMainFriending)
        }

        let friendingTemplate = document.querySelector('.original-friending')
        let newFriending = friendingTemplate.cloneNode(true)
        let parent = document.querySelector(`#basic-info`)
        parent.appendChild(newFriending)
        newFriending.classList.add(friendingClass)
        newFriending.classList.remove('original-friending')
    }

    if (friendingState == window.FRIENDING_STATE.Self) {
        return
    }
    processFormButtons();
    displayFriendingWithState(friendingState);


}
