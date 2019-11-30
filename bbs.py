from src.mapgro import BBS
from src.output import output, log_file

o = BBS('test_case/test_data_.csv', 5, 10, 13, 15)
print(output(o.compare_singleton_instances(o.infos)))
log_file(o.compare_singleton_instances(o.infos), 'test_case')