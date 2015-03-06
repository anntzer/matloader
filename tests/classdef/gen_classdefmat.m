simple = simpleclass;
save -v6 ../data/testclass_simple_6 simple;

hdl = simplehandle;
save -v6 ../data/testclass_hdl_6 hdl;

array = [simpleclass, simpleclass];
array(1).any_field_3 = 1;
save -v6 ../data/testclass_array_6 array;

ref = simpleclass;
ref.any_field_3 = anotherclass;
save -v6 ../data/testclass_ref_6 ref;

hdl_ref = simpleclass;
hdl_ref.any_field_3 = simplehandle;
save -v6 ../data/testclass_hdl_ref_6 hdl_ref;

exit;
