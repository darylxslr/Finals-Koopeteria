from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={
    r"/kopeetearia-api/*": {
        "origins": "http://localhost:5173"
    }
})

PORT = 8082

orders = []
id_counter = 1


@app.route("/kopeetearia-api/add-order", methods=["POST"])
def add_order():
    global id_counter
    data = request.get_json()

    order_name = data.get("orderName")
    price = data.get("price")
    discounted = data.get("discounted", False)

    if not order_name or price is None:
        return jsonify({
            "success": False,
            "message": "Order name and price are required",
            "data": None
        }), 400

    new_order = {
        "id": id_counter,
        "orderName": order_name,
        "price": price,
        "discounted": bool(discounted)
    }

    orders.append(new_order)
    id_counter += 1

    return jsonify({
        "success": True,
        "message": "Order added successfully",
        "data": new_order
    }), 201


@app.route("/kopeetearia-api/orders", methods=["GET"])
def get_orders():
    return jsonify({
        "success": True,
        "message": "Orders retrieved successfully",
        "data": orders
    })


@app.route("/kopeetearia-api/total-bill", methods=["GET"])
def total_bill():
    regular = sum(o["price"] for o in orders)
    discounted = sum(
        o["price"] * 0.95 if o["discounted"] else o["price"]
        for o in orders
    )

    return jsonify({
        "success": True,
        "message": "Total bill calculated",
        "data": {
            "regularBillTotal": regular,
            "discountedBillTotal": discounted
        }
    })


@app.route("/kopeetearia-api/update/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    data = request.get_json()
    order = next((o for o in orders if o["id"] == order_id), None)

    if not order:
        return jsonify({
            "success": False,
            "message": "Order not found",
            "data": None
        }), 404

    order["orderName"] = data.get("orderName", order["orderName"])
    order["price"] = data.get("price", order["price"])
    order["discounted"] = data.get("discounted", order["discounted"])

    return jsonify({
        "success": True,
        "message": "Order updated successfully",
        "data": order
    })


@app.route("/kopeetearia-api/delete/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    global orders
    orders = [o for o in orders if o["id"] != order_id]

    return jsonify({
        "success": True,
        "message": "Order deleted successfully",
        "data": None
    })


if __name__ == "__main__":
    print(f"✅ Backend running at http://localhost:{PORT}")
    app.run(port=PORT, debug=True)
