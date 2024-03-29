function addToCart(id, name, price) {
    fetch('/api/cart', {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then((data) => {
        console.info(data)
        let d = document.getElementsByClassName("cart-counter")
        for (let i = 0; i < d.length; i++)
            d[i].innerText = data.total_quantity
    }) // promise
}

function updateCart(bookId, obj) {
    fetch(`/api/cart/${bookId}`, {
        method: "put",
        body: JSON.stringify({
            "quantity": obj.value
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then((data) => {
            let d = document.getElementsByClassName("cart-counter")
            for (let i = 0; i < d.length; i++)
                d[i].innerText = data.total_quantity

            let a = document.getElementsByClassName("cart-amount")
            for (let i = 0; i < a.length; i++)
                a[i].innerText = data.total_amount.toLocaleString("en-US")
    }).catch(err => console.error(err))// promise
}

function deleteCart(bookId) {
    if (confirm("Bạn chắc chắn xóa không?") == true) {
        fetch(`/api/cart/${bookId}`, {
            method: "delete"
        }).then(res => res.json()).then((data) => {
            let d = document.getElementsByClassName("cart-counter")
            for (let i = 0; i < d.length; i++)
                d[i].innerText = data.total_quantity

            let a = document.getElementsByClassName("cart-amount")
            for (let i = 0; i < a.length; i++)
                a[i].innerText = data.total_amount.toLocaleString("en-US")

            let e = document.getElementById(`cart${bookId}`)
            e.style.display = "none"
        }).catch(err => console.error(err)) // promise
    }

}

function pay() {
    if (confirm("Bạn chắc chắn thanh toán không?")) {
        fetch("/api/pay").then(res => res.json()).then(data => {
            if (data.status === 200)
                window.location="/bill"
//                location.reload()
        })
    }
}

//function deleteSessoin(){
//    if (confirm("Bạn chắc chắn quay lại không?")) {
//        fetch("/bill/delete").then(res => res.json()).then(data => {
//            if (data.status === 200)
//                window.location="/"
////                location.reload()
//        })
//    }
//}

