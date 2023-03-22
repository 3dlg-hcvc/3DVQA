For each question we provide a dictionary containing the following information: `answer`, `answer_OBB`, `question_type`, `sub_question_type`, `object1`, `attribute1`, `relation`, `object2`, `attribute2`, `program`, and `extra_information`.  We summarize the fields below.

`question_type`, `sub_question_type`: `question_type` specifies the questions type and one of the following: `counting`, `location`, `query_attribute`, and `yes/no`.  The `sub_question_type` is `null` except for `yes/no` questions. In this case we subcategorize the questions into `existence`, `compare_integer`, and `check_relation` as the `sub_question_type`.

`object1`, `object2`: `object1` is the target object. It is the first object which appears in the question.
`object2` is the reference object. It is the second object which appears in the question. In the question *where is the chair with the same color as the table ?*, the *chair* is `object1` and the *table* is `object2`.

`attribute1`, `attribute2`: `attribute1` is the attribute associated with `object1`, and `attribute2` is associated with `object2`.
In the question *where is the short chair with the same color as the large table ?*, the *short* is `attribute1` and the *large* is `attribute2`.

`relation`:
It is the `relation` between `object1` and `object2`. In the question *where is the chair with the same color as the table ?*, *same color* is the relation. And in the question, *Is the chair next to the table ?* the `relation` would be *next to*.

`answer_id` provides the `id` of the relevant objects for the questions. Note that the ids can be used to get the original object instance segmentation as well as the OBBs for each object.  We describe the differences for the `answer_id` based on the question type.
  - `counting`: `answer_id` is the list of all the IDs we count towards answering the question.
  - `query_attribute`: `answer_id` consists of one ID related to the target object mentioned in the question.
  - `location`: `answer_id` consists of one ID related to the target object mentioned in the question.
  - `yes/no` (`existence`): `answer_id` is the list of all the IDs that ratifies the conditions in the question if there is any.
  - `yes/no` (`compare_integer`): `answer_id` consists of two lists, the first one consists of all IDs for the first object with the first attribute, and the second consists of all IDs of the second object with the second attribute.
  - `yes/no` (`check_relation`): `answer_id` consists of two IDs, the first one for the first object second one for the second object.

`extra_information`: additional information associated with each question that are not necessary for determining the answer.
  - `counting`: If there is only one unique item of the second object, in case of having an attribute for it, it is extra information. }
  - `query_attribute`: If there is only one unique item of the first object in the scene, in case of having an attribute for it, it is extra information. Also, if the target object can be found by the first attribute-object pair, then the second pair is extra information. Otherwise, if there is only one item of the second object, in case of having an attribute for it, it is extra information.}
  - `location`: If there is only one item of the first object, in case of having an attribute for it, it is extra information. Also if the target object can be found by only the first attribute-object pair, then the second pair is extra information. Else if there is only one item of the second object, in case of having the second attribute, it is extra information.
  - `yes/no` (`existence`):if there is only one item of the second object, in case of having an attribute for it, it is extra information. 
  - `yes/no` (`compare_integer`): extra information is not defined.
  - `yes/no` (`check_relation`): If there is only one item of the first object, in case of having attribute1, it is extra information. We have the same rule for the second object.

`programs`: For each question, we also provide functional programs that can be executed over the scene graph to compute the answer. Our programs are composed from the set of functions specified in CLEVR:
   - `filter(attr,objs)` Filters objects by specified attribute (color/height/volume).
   - `select(obj_cls)` Selects all objects from the class in the scene.
   - `relate(rel,objs)` Selects objects which refer with specified relation to the objects in the argument.
   - `count(objs)` Counts all objects in provided argument set. 
   - `measure(attr,objs)` Measures specified attribute of given object. 
   - `get_location(objs)` Outputs location of specified object.
   - `exists(objs)` Outputs *yes* if given set is not empty and *no* otherwise.
   - `compare_integer(int1,int2)` Outputs relation between integers (greater, equal or smaller).
   - `compare_attribute(attr1,attr2)` Compares attributes, outputting one of the categorical relations (bigger, wider, etc.).
