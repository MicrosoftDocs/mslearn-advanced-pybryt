The most basic kind of annotation in PyBryt is the value annotation, which asserts the presence of some value in the student's memory footprint. However, these annotations don't cover all cases; what if you want to check for two possible representations of some value, or you want to examine the ordering of values? This is where relational annotations come in.

Relational annotations define some kind of relationship between other annotations. You can think of relational annotations as annotations that operate on other annotations, asserting conditions on how those annotations are satisfied. In the last module, you learned about collection annotations, and how those can be used to enforce the ordering of annotations. Relational annotations are similar, and in fact collections can be thought of as a type of relational annotations.

Currently, PyBryt supports two types of relational annotations: temporal annotations and logical annotations.

## Temporal annotations

Temporal annotations describe a temporal relationship between different annotations. They are satisfied when all of their child annotations are satisfied and the timestamps of the values satisfying those annotations occur in a particular order.

PyBryt has only one kind of temporal annotation, the `BeforeAnnotation`, which asserts that the satisfying timestamps of its child annotations occur in non-decreasing order. These annotations can be instantiated directly using the constructor like any other annotations, but all annotations also have a `before` and `after` method that can be used to construct these annotations in a more semantic way:


```python
>>> a1 = pybryt.Value(1)
>>> a2 = pybryt.Value(2)
>>> a1.before(a2), a1.after(a2)
(pybryt.BeforeAnnotation, pybryt.BeforeAnnotation)
```

As you can see, both [`Annotation.before`](https://microsoft.github.io/pybryt/html/api_reference.html#pybryt.annotations.annotation.Annotation.before) and [`Annotation.after`](https://microsoft.github.io/pybryt/html/api_reference.html#pybryt.annotations.annotation.Annotation.after) return `BeforeAnnotation`s, but the ordering of the annotations is reversed in the annotation returned by `after`.

When you create a relational annotation, you can update the fields for each of the annotation options as needed, or pass the options as keyword arguments to the `before` or `after` method:


```python
a1_before_a2 = a1.before(
    a2,
    success_message="a1 is before a2",
    failure_message="a1 is not before a2",
)

# or:
a1_before_a2 = a1.before(a2)
a1_before_a2.success_message = "a1 is before a2"
a1_before_a2.failure_message = "a1 is not before a2"
```

With a dummy memory footprint, we can see how the `BeforeAnnotation` is satisfied. In the cell below, we create such a footprint using the `pybryt.MemoryFootprint.from_values` method, which accepts alternating values and timestamps:

```python
pybryt.MemoryFootprint.from_values(val1, ts1, val2, ts2, val3, ts3, ...)
```

Notice how the result of our relational annotation changes as we change the values in the footprint and their timestamps.


```python
>>> ref = pybryt.ReferenceImplementation("temporal-annotations", [a1_before_a2])
>>> # the values in the correct order
>>> res = ref.run(pybryt.MemoryFootprint.from_values(1, 1, 2, 2))
>>> print(pybryt.generate_report(res))
REFERENCE: temporal-annotations
SATISFIED: True
MESSAGES:
  - a1 is before a2
```

```python
>>> # put both values at the same timestamp
>>> res = ref.run(pybryt.MemoryFootprint.from_values(1, 1, 2, 1))
>>> print(pybryt.generate_report(res))
REFERENCE: temporal-annotations
SATISFIED: True
MESSAGES:
  - a1 is before a2
```

```python
>>> # put the timestamp of 1 after the timestamp of 2
>>> res = ref.run(pybryt.MemoryFootprint.from_values(1, 2, 2, 1))
>>> print(pybryt.generate_report(res))
REFERENCE: temporal-annotations
SATISFIED: False
MESSAGES:
  - a1 is not before a2
```

```python
>>> # don't satisfy the second annotation
>>> res = ref.run(pybryt.MemoryFootprint.from_values(1, 1))
>>> print(pybryt.generate_report(res))
REFERENCE: temporal-annotations
SATISFIED: False
MESSAGES:
  - a1 is not before a2
```

## Logical annotations

Logical annotations aren't concerned with the temporality of when annotations are satisfied but instead operate on whether annotations are satisfied at all. They assert conditions on whether child annotations are satisfied, allowing you to construct complex boolean logic within your references to allow for multiple paths arriving at the same solution.

To create a logic annotation, use Python's bitwise logical operators on any annotation:


```python
>>> a1 & a2, a1 | a2, a1 ^ a2
(pybryt.AndAnnotation, pybryt.OrAnnotation, pybryt.XorAnnotation)
```

To create conditions involving more than just two annotations, you can chain the operators, or instantiate the annotations directly with their child annotations. Similar to temporal annotations, the options for logical annotations can be set by updating the corresponding attribute on the 


```python
a3 = pybryt.Value(3)

all_anns = a1 & a2 & a3
all_anns.success_message = "Found a1, a2, and a3"
all_anns.failure_message = "Did not find a1, a2, and a3"

any_anns = a1 | a2 | a3
any_anns.success_message = "Found a1, a2, or a3"
any_anns.failure_message = "Did not find a1, a2, or a3"

one_ann = a1 ^ a2 ^ a3
one_ann.success_message = "Found exactly of a1, a2, or a3"
one_ann.failure_message = "Did not find exactly one of a1, a2, or a3"
```
