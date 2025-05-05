import json

class UserPreferences:
    def __init__(self, filepath="user_preferences.json"):
        self.filepath = filepath
        self.load_preferences()

    def load_preferences(self):
        try:
            with open(self.filepath, "r") as f:
                self.preferences = json.load(f)
        except FileNotFoundError:
            self.preferences = {}  # Initialize with empty preferences

    def save_preferences(self):
        with open(self.filepath, "w") as f:
            json.dump(self.preferences, f, indent=4)

    def get_user_preferences(self, user_id):
        return self.preferences.get(user_id, {"likes": [], "dislikes": []})

    def update_user_preferences(self, user_id, likes=None, dislikes=None):
        user_prefs = self.get_user_preferences(user_id)
        if likes:
            user_prefs["likes"].extend(likes)
            user_prefs["likes"] = list(set(user_prefs["likes"]))  # Remove duplicates
        if dislikes:
            user_prefs["dislikes"].extend(dislikes)
            user_prefs["dislikes"] = list(set(user_prefs["dislikes"])) # Remove duplicates
        self.preferences[user_id] = user_prefs
        self.save_preferences()

# Example usage:
if __name__ == "__main__":
    memory = UserPreferences()
    memory.update_user_preferences("user1", likes=["technology", "science"], dislikes=["gossip"])
    print(memory.get_user_preferences("user1"))