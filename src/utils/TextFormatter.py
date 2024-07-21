
class TextFormatter:
    def __init__(self):
        self.list = []

    def add(self, text, status):
        self.list.append((text, status))
    
    def format(self):
        self.formatted_list = []
        for descr, status in self.list:
            # Usa gli spazi non interrompibili per il riempimento
            padding = ' '
            self.formatted_list.append(f"{descr}{padding} {status}")
        return "\n".join(self.formatted_list)
 
    def printSummary(json, DB_status):
        # Initilize a text formatter object
        status = TextFormatter()
        if DB_status is True:
            status.add("<i>Transaction saved :</i>", "✅")
        else:
            status.add("<i>Transaction saved :</i>", "❌")
        status.add("<i>Transaction date :</i>", json["date"])
        status.add("<i>receipt ID :</i>", json["receipt_ID"])
        status.add("<i>Amount :</i>", json["total"])
        return status.format()
    
    def remove_last(self):
        self.list.pop()
