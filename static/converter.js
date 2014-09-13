if (!String.prototype.trim) {
    String.prototype.trim = function () {
        return this.replace(/^\s+|\s+$/g, '');
    };
}

function converter(){
    var text = document.getElementById("metadata_area").value;
    var check = 'Transaction Summary';

    if (text.indexOf(check) > -1){

        document.getElementById('demo').innerHTML = "InkFrog";
        var orderArray = text.split('Transaction Summary'),
            one = orderArray[0], two = orderArray[1].trim();
        var part_a = one.split('Ship to:'),
            a = part_a[0], b = part_a[1];
        a = a.split('\t');
        b = b.split('Shipping status');

        var product_info = two.split('\n')[1],
            product = product_info.split('\t');

        var order_dict = [];
        order_dict['Buyer'] = b[0].trim().split('\n')[0];
        order_dict['Buyername'] = a[1].split('(')[0];
        order_dict['Email'] = a[1].split('(')[1].replace(')','');
        order_dict['Buyer Address'] = b[0].trim();
        order_dict['Product'] =product[3] + ' x ' + product[2] + ' - ' + product[1];

        document.getElementById('id_product').value = order_dict['Product'];
        document.getElementById('id_buyer').value = order_dict['Buyer'];
        document.getElementById('id_buyername').value = order_dict['Buyername'];
        document.getElementById('id_address').value = order_dict['Buyer Address'];
        document.getElementById('id_buyeremail').value = order_dict['Email'];
    }

    else {
        document.getElementById('demo').innerHTML = "iBay365";
        var orderArray = text.split('买家'),
            one = orderArray[0], two = orderArray[1].trim();

        var order_dict = [];
        order_dict['Seller'] = one.split('(')[1].replace(')','');
        var buyer = two.split('Address')[0].split('\n');
        order_dict['Buyername'] = buyer[0].split(':')[1].split('(')[0].trim();
        order_dict['Buyer'] = buyer[0].split(':')[1].split('(')[1].replace(')','').trim();
        order_dict['Email'] = buyer[1].split(':')[1];

        order_dict['Address'] = two.split('Address:\t')[1].split('United States')[0].trim();
        order_dict['Product'] = two.split('价格\n')[1].split('\n')[0];


        //document.getElementById('demo').innerHTML =product;
        document.getElementById('id_buyername').value = order_dict['Buyername'];
        document.getElementById('id_seller').value = order_dict['Seller'];
        document.getElementById('id_buyer').value = order_dict['Buyer'];
        document.getElementById('id_buyeremail').value = order_dict['Email'];
        document.getElementById('id_address').value = order_dict['Address'];
        document.getElementById('id_product').value = order_dict['Product'];

    }

}

