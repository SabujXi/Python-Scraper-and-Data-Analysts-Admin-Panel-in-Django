import cli_app

from data.models import DataModel

all = DataModel.objects.all()

active_no_set = set()
for d in all:
    if d.active_no is None:
        pass
    else:
        if d.active_no in active_no_set:
            print("Duplicate active no %s " %d.active_no)
        active_no_set.add(d.active_no)
