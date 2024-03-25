import axios from "axios";

export const postNotification = (itemId, type, recipient, isUpdate) => {
    let message;
    if (isUpdate) {
      message = `${type} has been updated.`;
    } else {
      message = `You have been assigned to a new ${type} `;
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
        console.log("Notification posted successfully");
      })
      .catch((error) => {
        console.error("Error posting notification:", error);
      });
  };
