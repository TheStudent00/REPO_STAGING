# trace_compare.md

A trace is what a flow construct gives back instead of an
answer: the sequence of values at each joint, written in the
same bits encoding as an answer. That shared encoding is what
makes two languages' traces comparable at all.

Rewritten 2026-08-19 with log 038.

## the question this rewrite answers

Log 037 compared traces at ONE value per holder, so every for
loop it recorded walked the same three whole numbers. The
question it could not reach was whether a trace depends on the
VALUE. It does, and the dependence is measured below.

## go -- the for-iterable slot, by value class

```
holder 3  whole       steps 9
holder 4  whole       steps 9
holder 5  whole       steps 9
holder 6  whole       steps 9
holder 9  text        steps 1,5,9
holder 10 text        steps 2,4,5,9
holder 11 text        steps 1,5,9
holder 12 sequence    steps 2,3
holder 13 sequence    steps 2,3
holder 14 sequence    steps 2,3,5
holder 16 keyed       steps 1,2,3
holder 18 nesting     steps 1,2,3
holder 19 nesting     steps 1,2,4
```

## rust -- the for-iterable slot, by value class

```
holder 1  nothing     steps 0
holder 11 text        steps 0,2,4,5,9
holder 12 sequence    steps 0,2,3
holder 13 sequence    steps 0,2,3
holder 14 sequence    steps 0,2,3
holder 15 sequence    steps 0,2,3
holder 17 keyed       steps 0,1,2,3
holder 18 keyed       steps 0,1,2,3
holder 20 nesting     steps 1,2,3
```

## cpp -- the for-iterable slot, by value class

```
holder 10 text        steps 0,2,4,5,9
holder 12 text        steps 0,1,5,9
holder 13 sequence    steps 0,2,3
holder 14 sequence    steps 0,2,3
holder 15 sequence    steps 0,2,3
holder 16 sequence    steps 0,2,3
holder 17 sequence    steps 0,2,3
```

## swift -- the for-iterable slot, by value class

```
holder 9  text        steps 0,1,5,9
holder 10 text        steps 0,1,5,9
holder 11 text        steps 0,2,4,5,9
holder 12 text        steps 0,1,5,9
holder 13 sequence    steps 0,2,3
holder 14 sequence    steps 0,2,3
holder 15 sequence    steps 0,2,3
holder 17 sequence    steps 0,2,3
holder 18 keyed       steps 0,1,2,3
holder 21 nesting     steps 1,2,3
holder 22 nesting     steps 1,2
```

## dart -- the for-iterable slot, by value class

```
holder 10 text        steps 0,1,2,5,9
holder 11 text        steps 0,1,5,9
holder 13 sequence    steps 0,2,3,5
holder 14 sequence    steps 0,2,3,5
holder 15 sequence    steps 0,2,3,5
holder 16 sequence    steps 0,2,3,5
holder 22 nesting     steps 2,4
holder 24 nesting     steps 1,2,4
```

## csharp -- the for-iterable slot, by value class

```
holder 12 text        steps 0,1,2,5,9
holder 13 text        steps 0,1,2,5,9
holder 15 text        steps 0,2,4,5,9
holder 16 sequence    steps 0,2,3
holder 17 sequence    steps 0,2,3
holder 18 sequence    steps 0,2,3
holder 19 sequence    steps 0,2,3
holder 21 sequence    steps 0,1,2,3,5
holder 22 keyed       steps 0,1,2,3
holder 23 keyed       steps 0,1,2,3
holder 27 nesting     steps 1,2,3
holder 28 nesting     steps 1,2
holder 29 nesting     steps 1,2,4
```

## kotlin -- the for-iterable slot, by value class

```
holder 11 text        steps 0,1,2,5,9
holder 12 text        steps 0,1,2,5,9
holder 13 text        steps 0,1,2,5,9
holder 14 text        steps 0,2,4,5,9
holder 15 sequence    steps 0,2,3,5
holder 16 sequence    steps 0,2,3,5
holder 17 sequence    steps 0,2,3,5
holder 18 sequence    steps 0,3
holder 19 sequence    steps 0,2,3,5
holder 20 keyed       steps 0,1,2,3
holder 21 keyed       steps 0,1,2,3
holder 22 keyed       steps 0,1,2,3
holder 24 nesting     steps 1,2,4
```

## java -- the for-iterable slot, by value class

```
holder 15 text        steps 0,1,2,5,9
holder 17 text        steps 0,2,4,5,9
holder 18 sequence    steps 0,1,2,3,5
holder 19 sequence    steps 0,2,3
holder 20 sequence    steps 0,1,2,3,5
holder 21 sequence    steps 0,1,2,3
holder 22 sequence    steps 0,1,2,3,5
holder 23 sequence    steps 0,1,2,3
holder 29 nesting     steps 2,4
holder 31 nesting     steps 2,4
```

## typescript -- the for-iterable slot, by value class

```
holder 7  text        steps 0,1,5,9
holder 8  text        steps 0,1,5,9
holder 9  text        steps 0,2,4,5,9
holder 10 sequence    steps 0,1,2,3,5
holder 11 sequence    steps 0,1,2,3,5
holder 12 sequence    steps 0,1,2,3,5
holder 13 sequence    steps 0,1,2,3,5
holder 14 sequence    steps 0,1,3
holder 16 keyed       steps 0,1,2,3
holder 20 nesting     steps 2,4
holder 22 nesting     steps 2,4
```

## python -- the for-iterable slot, by value class

```
holder 9  text        steps 0,1,5,9
holder 10 text        steps 0,2,4,5,9
holder 11 text        steps 0,2,4,5,9
holder 12 sequence    steps 0,1,2,3,5
holder 13 sequence    steps 0,1,2,3,5
holder 14 sequence    steps 0,1,2,3,5
holder 15 sequence    steps 0,3
holder 16 sequence    steps 0,1,2,3,4
holder 17 keyed       steps 0,1,2,3
holder 18 keyed       steps 0,1,2,3
holder 20 keyed       steps 0,1,3
holder 21 nesting     steps 1,2,3
holder 22 nesting     steps 1,2
holder 23 nesting     steps 1,2,3
```

## ruby -- the for-iterable slot, by value class

```
holder 11 text        steps 0,1,5,9
holder 12 sequence    steps 0,1,2,3,5
holder 13 sequence    steps 0,1,2,3,5
holder 14 sequence    steps 0,1,2,3,5
holder 15 sequence    steps 0,1,2,3,5
holder 16 keyed       steps 0,1,2,3
holder 17 keyed       steps 0,1,2,3
holder 18 keyed       steps 0
holder 20 nesting     steps 1,2,3
holder 21 nesting     steps 1,2
```

## php -- the for-iterable slot, by value class

```
holder 0  nothing     steps 0
holder 1  truth       steps 0
holder 2  whole       steps 0
holder 4  whole       steps 0
holder 5  fractional  steps 0
holder 6  text        steps 0
holder 7  text        steps 0,2,4,5,9
holder 9  sequence    steps 0,1,2,3,5
holder 10 sequence    steps 0,1,2,3,5
holder 11 sequence    steps 0,1,2,3,5
holder 12 sequence    steps 0,1,2,3,5
holder 13 keyed       steps 0,1,2,3
holder 14 keyed       steps 0,1,2,3
holder 15 keyed       steps 0,1,2,3
holder 16 keyed       steps 0,1,2,3
holder 17 nesting     steps 1,2,3
holder 18 nesting     steps 1,2,3
```

