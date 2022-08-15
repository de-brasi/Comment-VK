from GUI import Interface
from Handler import Handler

application_handler = Handler()
application = Interface(application_handler)

application.view.mainloop()
