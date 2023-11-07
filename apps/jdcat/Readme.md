# VS java maven

в разы проще, и vs вроде работает нормально

## log4js

- https://www.dataset.com/blog/maven-log4j2-project/

## maven exec

https://www.baeldung.com/maven-java-main-method

```bash
mvn compile exec:java -Dexec.mainClass="com.example.Main"
```

## maven jar

- https://www.baeldung.com/executable-jar-with-maven

по этой ссылке использован 1 метод(maven-jar-plugin), работает

```bash
mvn package
java -jar ./target/demo-1.0-SNAPSHOT.jar
```

но не всё так радужно, зависимости кладутся в папку libs рядом с jarником, так что при переносе надо не забыть перенести и их

## other

- https://copyprogramming.com/howto/how-to-convert-the-object-to-string-in-java
- https://www.geeksforgeeks.org/java-swing-jlist-with-examples/
- https://www.codejava.net/java-core/the-java-language/java-8-lambda-listener-example
- https://www.digitalocean.com/community/tutorials/observer-design-pattern-in-java
