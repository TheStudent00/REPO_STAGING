# truthiness_table.md

The if-condition slot takes ONE operand. Run over every holder
and every value class, that single slot IS the cross-language
truthiness table. It is a one-operand table, so it is an
eight-form vector per language and never a sixty-four cell
grid.

Rewritten 2026-08-19 with log 038, when the nine checked
languages reached the value grain. Read the WORDS below before
the letters.

## the words used here

```
form
    the layer-1 name for a kind of value.
    there are eight of them.
holder grain
    every holder at ONE value, its base.
    log 037 measured the nine this way.
value grain
    every holder at EVERY value class.
    log 038 measures the nine this way.
splits
    the same slot sent some values to the
    then arm and some to the else arm.
```

## how to read a letter

```
T   always then
E   always else
S   splits: some values then, some else
R   refused: the checker would not take
    a value of that form in a condition
p   part refused: some holders of that
    form accepted, some not
X   raised at every value
H   the recorder refused, not the
    language
-   not probed
```

## the table, at the VALUE grain

Columns are the first two letters of the eight forms.

```
            no tr wh fr tx sq ke ne
go          R  S  R  R  R  R  R  R
rust        R  S  R  R  R  R  R  R
cpp         p  S  S  S  p  p  R  R
swift       R  S  R  R  R  R  R  R
dart        R  S  R  R  R  R  R  R
csharp      R  S  R  R  R  R  R  R
kotlin      R  S  R  R  R  R  R  R
java        R  S  R  R  R  R  R  R
typescript  p  S  S  S  S  T  T  T
python      E  S  S  S  S  S  S  T
ruby        E  S  T  T  T  T  T  T
php         E  S  S  S  S  S  S  T
```

## what MOVED from the holder grain

The nine checked languages only. The three open ones were
always at the value grain and cannot move.

```
            no tr wh fr tx sq ke ne
go           .  T>S  .   .   .   .   .   . 
rust         .  T>S  .   .   .   .   .   . 
cpp          .  T>S T>S T>S  .   .   .   . 
swift        .  T>S  .   .   .   .   .   . 
dart         .  T>S  .   .   .   .   .   . 
csharp       .  T>S  .   .   .   .   .   . 
kotlin       .  T>S  .   .   .   .   .   . 
java         .  T>S  .   .   .   .   .   . 
typescript   .  T>S T>S T>S T>S  .   .   . 
```

A cell reading `.` did not move. A cell reading `T>S` read
always-then at the holder grain and splits at the value grain.

