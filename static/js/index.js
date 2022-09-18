class RedirectToImage {
    constructor(params) {   
         this.params = params
    }

    cleanParams() {
        let params = this.params.slice(1)
        params = this.params.replaceAll('%20', ' ')
        return params
    }

    async ajaxRequest() {
        const url = window.location.href.split(window.location.pathname)[0]
        const request = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "X-Requested-With": "XMLHttpRequest",
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({
                    prompt_params: this.cleanParams()
                })
        })

        const response = await request.json()
        const image = JSON.parse(response.image)

        const create_image = document.createElement('img')
        create_image.src = `data:image/png;base64, ${image}`
        create_image.alt = 'Your AI generated image :)'
        document.body.appendChild(create_image)
        
        return 1
    }
}

window.onload = () => {
    const params = window.location.pathname
    if (params.length > 1) {
        const redirect = new RedirectToImage(params)
        redirect.ajaxRequest()
    }
}
