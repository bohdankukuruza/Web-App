// main/static/deps/js/jquery-ajax.js

$(document).ready(function () {
  // -------------------------
  // CSRF via cookie + header
  // -------------------------
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  const csrftoken = getCookie("csrftoken");

  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      const method = (settings.type || "").toUpperCase();
      if (!["GET", "HEAD", "OPTIONS", "TRACE"].includes(method)) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    },
  });

  // -------------------------
  // Notifications
  // -------------------------
  const $successMessage = $("#jq-notification");

  function showMessage(text) {
    if (!$successMessage.length) return;
    $successMessage.html(text || "");
    $successMessage.stop(true, true).fadeIn(250);
    setTimeout(function () {
      $successMessage.fadeOut(250);
    }, 3000);
  }

  // -------------------------
  // UI update
  // -------------------------
  function updateCartUI(data) {
    if (
      $("#cart-items-container-modal").length &&
      data.cart_items_html_modal !== undefined
    ) {
      $("#cart-items-container-modal").html(data.cart_items_html_modal);
    }

    if (
      $("#cart-items-container-page").length &&
      data.cart_items_html_page !== undefined
    ) {
      $("#cart-items-container-page").html(data.cart_items_html_page);
    }

    if (data.cart_total_quantity !== undefined) {
      $("#goods-in-cart-count").text(data.cart_total_quantity);
    }
  }

  function ajaxError(context, xhr) {
    console.log(
      context + " AJAX error:",
      xhr.status,
      xhr.responseText || xhr.statusText
    );
  }

  // -------------------------
  // Cart API helpers
  // -------------------------
  function postJson(url, payload, onSuccess, contextName) {
    $.ajax({
      type: "POST",
      url: url,
      dataType: "json",
      data: payload,
      success: function (data) {
        onSuccess && onSuccess(data);
      },
      error: function (xhr) {
        ajaxError(contextName || "ajax", xhr);
      },
    });
  }

  function updateCart(cartID, quantity, url) {
    postJson(
      url,
      {
        cart_id: cartID,
        quantity: quantity,
      },
      function (data) {
        showMessage(data.message);
        updateCartUI(data);
      },
      "cart_change"
    );
  }

  // -------------------------
  // ADD TO CART (prevent double fire)
  // -------------------------
  $(document)
    .off("click.cart", ".add-to-cart")
    .on("click.cart", ".add-to-cart", function (e) {
      e.preventDefault();

      const $btn = $(this);

      // защита от двойного клика
      if ($btn.data("busy")) return;
      $btn.data("busy", true);

      const product_id = $btn.data("product-id");
      const url = $btn.attr("href");

      postJson(
        url,
        { product_id: product_id },
        function (data) {
          showMessage(data.message);
          updateCartUI(data);
        },
        "add-to-cart"
      );

      // снимаем блокировку через короткое время
      setTimeout(function () {
        $btn.data("busy", false);
      }, 350);
    });

  // -------------------------
  // REMOVE FROM CART
  // -------------------------
  $(document)
    .off("click.cart", ".remove-from-cart")
    .on("click.cart", ".remove-from-cart", function (e) {
      e.preventDefault();

      const $btn = $(this);

      if ($btn.data("busy")) return;
      $btn.data("busy", true);

      const cart_id = $btn.data("cart-id");
      const url = $btn.attr("href");

      postJson(
        url,
        { cart_id: cart_id },
        function (data) {
          showMessage(data.message);
          updateCartUI(data);
        },
        "remove-from-cart"
      );

      setTimeout(function () {
        $btn.data("busy", false);
      }, 350);
    });

  // -------------------------
  // DECREMENT
  // -------------------------
  $(document)
    .off("click.cart", ".decrement")
    .on("click.cart", ".decrement", function (e) {
      e.preventDefault();

      const $btn = $(this);

      if ($btn.data("busy")) return;
      $btn.data("busy", true);

      const url = $btn.data("cart-change-url");
      const cartID = $btn.data("cart-id");

      const $input = $btn.closest(".input-group").find(".number");
      let currentValue = parseInt($input.val(), 10);
      if (isNaN(currentValue)) currentValue = 1;

      if (currentValue > 1) {
        const newValue = currentValue - 1;
        $input.val(newValue);
        updateCart(cartID, newValue, url);
      }

      setTimeout(function () {
        $btn.data("busy", false);
      }, 200);
    });

  // -------------------------
  // INCREMENT
  // -------------------------
  $(document)
    .off("click.cart", ".increment")
    .on("click.cart", ".increment", function (e) {
      e.preventDefault();

      const $btn = $(this);

      if ($btn.data("busy")) return;
      $btn.data("busy", true);

      const url = $btn.data("cart-change-url");
      const cartID = $btn.data("cart-id");

      const $input = $btn.closest(".input-group").find(".number");
      let currentValue = parseInt($input.val(), 10);
      if (isNaN(currentValue)) currentValue = 0;

      const newValue = currentValue + 1;
      $input.val(newValue);
      updateCart(cartID, newValue, url);

      setTimeout(function () {
        $btn.data("busy", false);
      }, 200);
    });

  // -------------------------
  // Django alert notification close
  // -------------------------
  const $notification = $("#notification");
  if ($notification.length > 0) {
    setTimeout(function () {
      $notification.alert("close");
    }, 7000);
  }

  // -------------------------
  // Modal open/close
  // -------------------------
  $("#modalButton")
    .off("click.cart")
    .on("click.cart", function () {
      $("#exampleModal").appendTo("body");
      $("#exampleModal").modal("show");
    });

  $("#exampleModal .btn-close")
    .off("click.cart")
    .on("click.cart", function () {
      $("#exampleModal").modal("hide");
    });

  // -------------------------
  // Delivery field toggle
  // -------------------------
  $(document)
    .off("change.cart", "input[name='requires_delivery']")
    .on("change.cart", "input[name='requires_delivery']", function () {
      const selectedValue = $(this).val();
      if (selectedValue === "1") {
        $("#deliveryAddressField").show();
      } else {
        $("#deliveryAddressField").hide();
      }
    });
});