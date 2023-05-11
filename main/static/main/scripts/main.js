import { processProfile } from "./profile.js";

window.SectionEnum = {
    'Profile': 'profile',
    'Search': 'search',
}

const sectionMainMap = {
    'profile': document.querySelector('#section-profile'),
    'search': document.querySelector('#section-search')
};

function setMainSection(sectionName = 'profile') {
    if (!(sectionName in sectionMainMap)) {
        console.log("ERROR!! INVALID SECTION NAME!!")
    }
    for (const [name, section] of Object.entries(sectionMainMap)) {
        if (name == sectionName) {
            section.style.display = 'block'
        } else {
            section.style.display = 'none'
        }
    }
}

function resetSearch() {
    let searchForm = document.querySelector('#search-bar form')
    searchForm.style.display = 'none'
}

function processSearch(searchUrl) {
    axios.get(searchUrl, {
        params: {}
    })
        .then(function (response) {
            if (response.data.error) {
                console.log('ERROR!')
                console.log(response.data.error)
                return
            }
            console.log('Search - SUCCESS!!');
            console.log(response.data.user_list)
            // process(response.data.user_list)
            // return response.data.user_list
        })
        .catch(function (err) {
            console.log('FAILURE!!');
            console.log(err)
        });
}

export function mainProcessSearch(searchUrl, title = 'Facebook - Search', mainUrl = window.location.href) {
    console.log("process search")
    setMainSection(window.SectionEnum.Search)
    processSearch(searchUrl)
    document.title = title
    window.history.pushState({ 'search_url': searchUrl, 'section': window.SectionEnum.Search, 'title': title }, "", mainUrl);
    console.log(window.history)
}

function mainProcessProfile(profileUrl, title, mainUrl) {
    console.log("process profile")

    setMainSection()
    processProfile(profileUrl)
    document.title = title
    window.history.pushState({ 'profile_url': profileUrl, 'section': window.SectionEnum.Profile, 'title': title }, "", mainUrl);
    console.log(window.history)

}


mainProcessProfile(window.secondUserMainUrl + '/profile', 'Facebook - profile', window.secondUserMainUrl)

export function processProfileLink(link, procesProfile = processProfile) {
    link.addEventListener('click', e => {
        e.preventDefault()
        e.stopPropagation()
        mainProcessProfile(`${link.href}/profile`, 'Facebook - profile', link.href)
    })
}

window.onpopstate = function (e) {
    // console.log(e)
    if (e.state) {
        console.log("HAS STATE!!")
        console.log(e.state)
        if (e.state.section == window.SectionEnum.Profile) {
            resetSearch()
            setMainSection(window.SectionEnum.Profile)
            processProfile(e.state.profile_url);
            document.title = e.state.title;
        } else if (e.state.section == window.SectionEnum.Search) {
            console.log('e state search')
            console.log(e.state)
            setMainSection(window.SectionEnum.Search)
            processSearch(e.state.search_url);
            document.title = e.state.title;
        }
    } else {
        console.log("GO BACK!!")
        // window.history.back()
    }
};