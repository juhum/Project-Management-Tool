import axios from "axios";

export const postNotification = (itemId, type, recipient, isUpdate) => {
    let message;
    if (isUpdate) {
      message = `The ${type} (${itemId}) has been updated.`;
    } else {
      message = `New ${type} created: ${itemId}`;
    }
  
    const notificationData = {
      message: message,
      recipients: recipient,
    };
  
    if (type === "project") {
      notificationData.project = itemId;
    } else if (type === "task") {
      notificationData.task = itemId;
    }
  
    axios
      .post("/api/v1/notifications/", notificationData, {
        headers: {
          Authorization: `token ${localStorage.token}`,
        },
      })
      .then((response) => {
        console.log("Notification posted successfully:", response.data);
      })
      .catch((error) => {
        console.error("Error posting notification:", error);
      });
  };
