class Publisher:
    def __init__(self):
        # List to hold all the subscribers (observers)
        self._subscribers = []

    def subscribe(self, observer):
        """Adds an observer to the list of subscribers."""
        if observer not in self._subscribers:
            self._subscribers.append(observer)
            print(f"Subscribed: {observer}")

    def unsubscribe(self, observer):
        """Removes an observer from the list of subscribers."""
        if observer in self._subscribers:
            self._subscribers.remove(observer)
            print(f"Unsubscribed: {observer}")

    def notify(self, **kwargs):
        """Notifies all subscribers that a change has occurred with the provided keyword arguments."""
        for observer in self._subscribers:
            observer.update(**kwargs)  # Pass the keyword arguments to the observer's update method
            print(f"Notified: {observer}")
